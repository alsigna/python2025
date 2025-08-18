import asyncio
from time import perf_counter

import aiohttp

NETBOX_TOKEN = "734e96018b4dfe18716e24d3e7b4b32adbb4ad80"
NETBOX_URL = "https://demo.netbox.dev"
NETBOX_HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "demo-python2025",
}
CONNECTION_LIMIT = 100


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def get_devices_id_wrong() -> list[int]:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=CONNECTION_LIMIT,
            ssl=False,
        ),
        headers=NETBOX_HEADERS,
        base_url=NETBOX_URL,
    ) as session:
        async with session.get(
            url="/api/dcim/devices/",
            params=[
                ("brief", "true"),
                ("limit", 1000),
            ],
        ) as response:
            response.raise_for_status()
            response_json = await response.json()

    result = [device["id"] for device in response_json["results"]]
    log(f"get_devices_id_wrong id устройств получены, всего {len(result)}")
    return result


async def get_devices_id_ok(session: aiohttp.ClientSession) -> list[int]:
    async with session.get(
        url="/api/dcim/devices/",
        params=[
            ("brief", "true"),
            ("limit", 1000),
        ],
    ) as response:
        response_json = await response.json()

    result = [device["id"] for device in response_json["results"]]
    log(f"get_devices_id_wrong id устройств получены, всего {len(result)}")
    return result


async def fetch_device_name_wrong(device_id: int) -> list[str]:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=CONNECTION_LIMIT,
            ssl=False,
        ),
        headers=NETBOX_HEADERS,
        base_url=NETBOX_URL,
    ) as session:
        async with session.get(
            url=f"/api/dcim/devices/{device_id}/",
        ) as response:
            response.raise_for_status()
            response_json = await response.json()

    name = response_json["name"] or "unknown"
    log(f"имя для устройства {device_id} получено: {name}")
    return name


async def fetch_device_name_ok(session: aiohttp.ClientSession, device_id: int) -> list[str]:
    async with session.get(
        url=f"/api/dcim/devices/{device_id}/",
    ) as response:
        response_json = await response.json()

    name = response_json["name"] or "unknown"
    log(f"имя для устройства {device_id} получено: {name}")
    return name


async def main_wrong() -> None:
    devices_id = await get_devices_id_wrong()
    tasks = [
        asyncio.create_task(
            fetch_device_name_wrong(device_id),
        )
        for device_id in devices_id
    ]
    names = await asyncio.gather(*tasks)
    print("\n".join(names))


async def main_ok() -> None:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=CONNECTION_LIMIT,
            limit_per_host=CONNECTION_LIMIT,
            ssl=False,
        ),
        raise_for_status=True,
        headers=NETBOX_HEADERS,
        base_url=NETBOX_URL,
    ) as session:
        devices_id = await get_devices_id_ok(session)
        tasks = [asyncio.create_task(fetch_device_name_ok(session, device_id)) for device_id in devices_id]
        names = await asyncio.gather(*tasks)
    print("\n".join(names))


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main_wrong())
    # asyncio.run(main_ok())
    log("асинхронный код закончен")
