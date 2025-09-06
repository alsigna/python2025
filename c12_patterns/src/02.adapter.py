from io import TextIOWrapper
from typing import Any, Literal

import yaml


class Device:
    def __init__(self, hostname: str) -> None:
        self.hostname = hostname

    def get_info(self) -> dict[str, str]:
        return {
            "eth1": "192.168.1.1/24",
            "eth2": "192.168.2.1/24",
        }

    def write_to_file(self, data: dict[str, Any], f: TextIOWrapper) -> None:
        yaml.safe_dump(data, f)


class SoT:
    DEVICES = {
        1: {"hostname": "rt1"},
        2: {"hostname": "rt2"},
    }
    INTERFACES = {
        101: {"device_id": 1, "name": "eth1", "ip": "192.168.1.1/24"},
        102: {"device_id": 1, "name": "eth2", "ip": "192.168.2.1/24"},
        103: {"device_id": 2, "name": "eth1", "ip": "192.168.3.1/24"},
    }

    @classmethod
    def request(cls, obj: Literal["device", "interface"]) -> dict[int, dict[str, Any]]:
        match obj:
            case "device":
                return cls.DEVICES
            case "interface":
                return cls.INTERFACES


class DeviceSoT(Device, SoT):
    def _device_id_by_hostname(self, data: dict[int, Any], hostname: str) -> int:
        for id_, params in data.items():
            if params.get("hostname") == hostname:
                return id_
        return 0

    def _interfaces_by_device_id(self, data: dict[int, Any], device_id: int) -> list[tuple[str, str]]:
        result = []
        for params in data.values():
            if params.get("device_id") == device_id:
                result.append((params.get("name"), params.get("ip")))
        return result

    def get_info(self) -> dict[str, str]:
        device_id = self._device_id_by_hostname(self.request("device"), self.hostname)
        interfaces = self._interfaces_by_device_id(self.request("interface"), device_id)
        data = dict(interfaces)
        return data


if __name__ == "__main__":
    rt1 = Device("rt1")
    data = rt1.get_info()
    with open("r1.yaml", "w") as f:
        rt1.write_to_file(
            {
                "hostname": rt1.hostname,
                "interfaces": data,
            },
            f,
        )

    rt2 = DeviceSoT("rt2")
    data = rt2.get_info()
    with open("r2.yaml", "w") as f:
        rt2.write_to_file(
            {
                "hostname": rt2.hostname,
                "interfaces": data,
            },
            f,
        )
