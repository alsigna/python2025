import json
from collections.abc import Callable
from enum import StrEnum, auto
from typing import Literal, Self, cast


class Platform(StrEnum):
    CISCO_IOSXE = auto()
    HUAWEI_VRP = auto()


class SaveLoadMixIn:
    def save(self, filename: str) -> None:
        method_name = "_serialize"
        method = getattr(self, method_name, None)
        if method is None:
            raise AttributeError(f"класс должен иметь метод {method_name}()")

        data: str = method()
        with open(filename, "w") as f:
            f.write(data)

    @classmethod
    def load(cls, filename: str) -> Self:
        method_name = "_deserialize"
        method = getattr(cls, method_name, None)
        if method is None:
            raise AttributeError(f"класс должен иметь метод {method_name}()")

        with open(filename, "r") as f:
            data = f.read()
        obj: Self = method(data)
        return obj


class Device(SaveLoadMixIn):
    __slots__ = ("ip", "platform", "_location")

    def __init__(self, ip: str, platform: Platform):
        self.ip = ip
        self.platform = platform
        self._location: str

    @property
    def location(self) -> str:
        if getattr(self, "_location", None) is None:
            print(" >> обновляем значение location")
            self._location = self._get_netbox_location_by_ip(self.ip)
        return self._location

    def _get_netbox_location_by_ip(self, ip: str) -> str:
        return "dc" if ip.startswith("10.") else "campus"

    def _serialize(self) -> str:
        return json.dumps(
            {
                "ip": self.ip,
                "platform": self.platform,
                "location": getattr(self, "_location", None),
            },
        )

    @classmethod
    def _deserialize(cls, data: str) -> Self:
        json_data = json.loads(data)
        obj = cls(
            ip=json_data["ip"],
            platform=Platform(json_data["platform"]),
        )
        obj._location = json_data["location"]
        return obj


if __name__ == "__main__":
    device = Device("101.0.0.1", Platform.CISCO_IOSXE)
    print(device.ip)
    print(device.platform)
    print(device.location)
    device.save("test.txt")
    print("-" * 10)
    new_device = Device.load("test.txt")
    print(new_device.ip)
    print(new_device.platform)
    print(new_device.location)
