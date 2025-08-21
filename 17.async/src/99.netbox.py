import asyncio
import json
from time import perf_counter
from types import TracebackType
from typing import Any, Self

import aiohttp
from pydantic import BaseModel

NETBOX_TOKEN = "8a11fb6aa8f3918cb05e984cf4c16ad5a02e2678"
NETBOX_URL = "https://demo.netbox.dev"

NETBOX_DEVICES = [
    {
        "name": "r01",
        "model": "iosv",
        "role": "router",
        "site": "dm-akron",
        "ip-addresses": {"192.168.122.101/24": "Loopback0"},
        "tags": ["python2025"],
    },
    {
        "name": "r02",
        "model": "iosv",
        "role": "router",
        "site": "dm-akron",
        "ip-addresses": {"192.168.122.102/24": "Loopback0"},
        "tags": ["python2025"],
    },
    {
        "name": "r03",
        "model": "usg6000v2",
        "role": "router",
        "site": "dm-akron",
        "ip-addresses": {"192.168.122.103/24": "Loopback0"},
        "tags": ["python2025"],
    },
]

NETBOX_DEVICE_TYPES = [
    {
        "manufacturer": "cisco",
        "model": "IOSv",
        "slug": "iosv",
    },
    {
        "manufacturer": "huawei",
        "model": "USG6000V2",
        "slug": "usg6000v2",
    },
]


class NetboxDeviceType(BaseModel):
    pass


class NetboxIP(BaseModel):
    address: str
    id: int = 0
    role: str = "loopback"
    assigned_object_type: str = "dcim.interface"
    assigned_object_id: int = 0


class NetboxInterface(BaseModel):
    name: str
    id: int = 0
    type: str = "virtual"
    device_id: int = 0
    ip_addresses: list[NetboxIP] = []


class NetboxDevice(BaseModel):
    id: int = 0
    name: str
    status: str = "decommissioning"
    role: str
    role_id: int = 0
    site: str
    site_id: int = 0
    device_type: str
    device_type_id: int = 0
    interfaces: list[NetboxInterface] = []
    tags_id: list[int] = []


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class NetboxAPIHandler:
    def __init__(self, base_url: str, token: str, session_limit: int = 10) -> None:
        self.base_url = base_url
        self.token = token
        self.session_limit = session_limit
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=self.session_limit,
                ssl=False,
            ),
            base_url=self.base_url,
            # raise_for_status=True,
            headers={
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "demo-python2025",
            },
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        await self.session.close()
        self.session = None

    async def get(self, url: str, params: list[tuple[str, Any]] | None = None):
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")
        async with self.session.get(url=url, params=params) as response:
            response.raise_for_status()
            response_json = await response.json()

        if "results" not in response_json:
            return [response_json]

        result: list = response_json.get("results", [])
        while (url := response_json.get("next")) is not None:
            async with self.session.get(url=url) as response:
                response.raise_for_status()
                response_json = await response.json()
                result.extend(response_json.get("results", []))

        return result

    async def post(self, url: str, data: dict[str, Any]):
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")
        async with self.session.post(url=url, data=json.dumps(data)) as response:
            response.raise_for_status()
            response_json = await response.json()
        return response_json

    async def patch(self, url: str, data: dict[str, Any]):
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")
        async with self.session.patch(url=url, data=json.dumps(data)) as response:
            response.raise_for_status()
            response_json = await response.json()
        return response_json


class NetboxObjectCreator:
    @staticmethod
    async def _get_objects_id(netbox: NetboxAPIHandler, url: str, attr: str = "slug") -> dict[str, int]:
        objs = await netbox.get(
            url=url,
            params=[("brief", "true"), ("limit", 10)],
        )
        return {obj[attr]: obj["id"] for obj in objs}

    @classmethod
    async def _get_device_roles(cls, netbox: NetboxAPIHandler) -> dict[str, int]:
        return await cls._get_objects_id(netbox, "/api/dcim/device-roles/")

    @classmethod
    async def _get_device_type_ids(cls, netbox: NetboxAPIHandler) -> dict[str, int]:
        return await cls._get_objects_id(netbox, "/api/dcim/device-types/")

    @classmethod
    async def _get_manufacturer_ids(cls, netbox: NetboxAPIHandler) -> dict[str, int]:
        return await cls._get_objects_id(netbox, "/api/dcim/manufacturers/")

    @classmethod
    async def _get_tags_ids(cls, netbox: NetboxAPIHandler) -> dict[str, int]:
        return await cls._get_objects_id(netbox, "/api/extras/tags/")

    @classmethod
    async def _get_sites(cls, netbox: NetboxAPIHandler) -> dict[str, int]:
        return await cls._get_objects_id(netbox, "/api/dcim/sites/")

    @classmethod
    async def _fill_existed_objects(cls, netbox: NetboxAPIHandler, devices: dict[str, str]) -> list[NetboxDevice]:
        device_roles, device_types, sites, tags = await asyncio.gather(
            asyncio.create_task(cls._get_device_roles(netbox)),
            asyncio.create_task(cls._get_device_type_ids(netbox)),
            asyncio.create_task(cls._get_sites(netbox)),
            asyncio.create_task(cls._get_tags_ids(netbox)),
        )
        result = []
        for device in devices:
            interfaces: dict[str, NetboxInterface] = {}
            for ip, intf in device["ip-addresses"].items():
                nb_intf = interfaces.get(intf)
                if nb_intf is None:
                    nb_intf = NetboxInterface(name=intf)
                    interfaces[intf] = nb_intf
                nb_intf.ip_addresses.append(NetboxIP(address=ip))

            nb_device = NetboxDevice(
                name=device["name"],
                role=device["role"],
                role_id=device_roles[device["role"]],
                site=device["site"],
                site_id=sites[device["site"]],
                device_type=device["model"],
                device_type_id=device_types[device["model"]],
                interfaces=interfaces.values(),
                tags_id=[tags[tag] for tag in device["tags"]],
            )
            result.append(nb_device)
        return result

    @classmethod
    async def _create_devices(cls, netbox: NetboxAPIHandler, devices: list[NetboxDevice]) -> list[NetboxDevice]:
        result = [device.model_copy(deep=True) for device in devices]
        to_create = [
            {
                "name": device.name,
                "device_type": device.device_type_id,
                "role": device.role_id,
                "status": device.status,
                "site": device.site_id,
                "tags": device.tags_id,
            }
            for device in result
        ]
        created_devices = await netbox.post("/api/dcim/devices/", to_create)
        created_device_ids = {device["name"]: device["id"] for device in created_devices}
        for device in result:
            device.id = created_device_ids[device.name]
            for interface in device.interfaces:
                interface.device_id = created_device_ids[device.name]
        return result

    @classmethod
    async def _create_interfaces(cls, netbox: NetboxAPIHandler, devices: list[NetboxDevice]) -> list[NetboxDevice]:
        result = [device.model_copy(deep=True) for device in devices]
        to_create = [
            {
                "name": interface.name,
                "device": device.id,
                "type": interface.type,
            }
            for device in result
            for interface in device.interfaces
        ]
        created_interfaces = await netbox.post("/api/dcim/interfaces/", to_create)
        for interface in created_interfaces:
            intf_id = interface["id"]
            intf_name = interface["name"]
            device_id = interface["device"]["id"]
            for device in result:
                if device.id != device_id:
                    continue
                for intf in device.interfaces:
                    if intf.name != intf_name:
                        continue
                    intf.id = intf_id
                    for ip in intf.ip_addresses:
                        ip.assigned_object_id = intf_id
        return result

    @classmethod
    async def _create_ip_addresses(cls, netbox: NetboxAPIHandler, devices: list[NetboxDevice]) -> list[NetboxDevice]:
        result = [device.model_copy(deep=True) for device in devices]
        to_create = [
            {
                "address": ip.address,
                "assigned_object_id": ip.assigned_object_id,
                "assigned_object_type": ip.assigned_object_type,
                "role": ip.role,
            }
            for device in result
            for interface in device.interfaces
            for ip in interface.ip_addresses
        ]
        created_ips = await netbox.post("/api/ipam/ip-addresses/", to_create)
        for ip in created_ips:
            ip_id = ip["id"]
            ip_address = ip["address"]
            intf_id = ip["assigned_object_id"]
            device_id = ip["assigned_object"]["device"]["id"]
            for device in result:
                if device.id != device_id:
                    continue
                for intf in device.interfaces:
                    if intf.id != intf_id:
                        continue
                    for ip in intf.ip_addresses:
                        if ip.address != ip_address:
                            continue
                        ip.id = ip_id

        return result

    @classmethod
    async def _set_primary_ip(cls, netbox: NetboxAPIHandler, devices: list[NetboxDevice]) -> None:
        to_update = [
            {
                "id": device.id,
                "primary_ip4": device.interfaces[0].ip_addresses[0].id,
            }
            for device in devices
        ]
        await netbox.patch("/api/dcim/devices/", to_update)

    @classmethod
    async def _create_tags(cls, netbox: NetboxAPIHandler) -> None:
        existed_tags = await cls._get_tags_ids(netbox)
        needed_tags: set[str] = set()
        for device in NETBOX_DEVICES:
            needed_tags.update(device.get("tags", []))
        to_create = []
        for tag in needed_tags:
            if tag in existed_tags:
                continue
            to_create.append(
                {
                    "name": tag,
                    "slug": tag.lower(),
                },
            )
        if len(to_create) == 0:
            return
        else:
            await netbox.post("/api/extras/tags/", to_create)

    @classmethod
    async def _create_device_type(cls, netbox: NetboxAPIHandler) -> None:
        device_types, manufacturers = await asyncio.gather(
            asyncio.create_task(cls._get_device_type_ids(netbox)),
            asyncio.create_task(cls._get_manufacturer_ids(netbox)),
        )

        to_create = []
        for device_type in NETBOX_DEVICE_TYPES:
            slug = device_type.get("slug")
            if slug in device_types:
                continue
            if device_type["manufacturer"] not in manufacturers:
                new_manufacturer = await netbox.post(
                    "/api/dcim/manufacturers/",
                    {
                        "name": device_type["manufacturer"].title(),
                        "slug": device_type["manufacturer"].lower(),
                    },
                )
                manufacturers |= {new_manufacturer["slug"]: new_manufacturer["id"]}
            to_create.append(
                {
                    "manufacturer": manufacturers[device_type["manufacturer"]],
                    "model": device_type["model"],
                    "slug": device_type["slug"],
                    "part_number": device_type["model"],
                    "is_full_depth": False,
                },
            )

        if len(to_create) == 0:
            return

        await netbox.post("/api/dcim/device-types/", to_create)

    @classmethod
    async def populate_netbox(cls, devices: list[dict[str, str]]) -> dict[str, int]:
        async with NetboxAPIHandler(
            base_url=NETBOX_URL,
            token=NETBOX_TOKEN,
        ) as netbox:
            await cls._create_device_type(netbox)
            await cls._create_tags(netbox)
            netbox_devices = await cls._fill_existed_objects(netbox, devices)
            netbox_devices = await cls._create_devices(netbox, netbox_devices)
            netbox_devices = await cls._create_interfaces(netbox, netbox_devices)
            netbox_devices = await cls._create_ip_addresses(netbox, netbox_devices)
            await cls._set_primary_ip(netbox, netbox_devices)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(NetboxObjectCreator.populate_netbox(NETBOX_DEVICES))
    log("асинхронный код закончен")
