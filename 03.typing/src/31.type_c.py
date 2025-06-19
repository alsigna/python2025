from abc import ABC, abstractmethod
from enum import StrEnum, auto
from typing import Any, Protocol, cast

from scrapli import Scrapli

type ScrapliDict = dict[str, Any]


class Transport(StrEnum):
    SYSTEM = auto()
    TELNET = auto()
    PARAMIKO = auto()


class Platform(StrEnum):
    HUAWEI_VRP = auto()
    CISCO_IOSXE = auto()
    ARISTA_EOS = auto()


class Device(ABC):
    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        transport: Transport = Transport.SYSTEM,
    ) -> None:
        self.hostname = hostname
        self._username = username
        self._password = password
        self._transport = transport
        self._cli: Scrapli = Scrapli(**self._scrapli)

    @property
    @abstractmethod
    def show_version_command(self) -> str: ...

    @property
    @abstractmethod
    def platform(self) -> Platform: ...

    @property
    def _scrapli(self) -> ScrapliDict:
        return {
            "auth_username": self._username,
            "auth_password": self._password,
            "auth_secondary": self._password,
            "platform": self.platform,
            "transport": self._transport,
            "host": self.hostname,
        }

    def show_version(self) -> None:
        print("-" * 10)
        print(f"устройство: {self.hostname}")
        print(f"платформа: {self.platform}")
        print(f"команда: {self.show_version_command}")


class AristaEOS(Device):
    show_version_command = "show version"
    platform = Platform.ARISTA_EOS


class HuaweiVRP(Device):
    show_version_command = "display version"
    platform = Platform.HUAWEI_VRP


class DeviceFactory:
    _PLATFORM_MAP: dict[str, type[Device]] = {
        Platform.ARISTA_EOS: AristaEOS,
        Platform.HUAWEI_VRP: HuaweiVRP,
    }

    @classmethod
    def create(
        cls,
        hostname: str,
        username: str,
        password: str,
        platform: Platform,
        transport: Transport = Transport.SYSTEM,
    ) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](
            hostname=hostname,
            username=username,
            password=password,
            transport=transport,
        )


# class Device(DeviceABC):
#     _PLATFORM_MAP: dict[str, type[DeviceABC]] = {
#         Platform.ARISTA_EOS: AristaEOS,
#         Platform.HUAWEI_VRP: HuaweiVRP,
#     }

#     def __new__(
#         cls,
#         hostname: str,
#         username: str,
#         password: str,
#         platform: Platform,
#         transport: Transport = Transport.SYSTEM,
#     ) -> "Device":
#         if platform not in cls._PLATFORM_MAP:
#             raise ValueError(f"неизвестная платформа '{platform}'")
#         _device_class: type[DeviceABC] = cls._PLATFORM_MAP[platform]
#         device = _device_class(
#             hostname=hostname,
#             username=username,
#             password=password,
#             transport=transport,
#         )
#         device = cast(Device, device)
#         return device


if __name__ == "__main__":
    devices: list[Device] = [
        DeviceFactory.create(
            hostname="192.168.0.1",
            username="admin",
            password="P@ssw0rd",
            platform=Platform.ARISTA_EOS,
        ),
        DeviceFactory.create(
            hostname="192.168.0.2",
            username="admin",
            password="P@ssw0rd",
            platform=Platform.HUAWEI_VRP,
        ),
    ]
    for device in devices:
        device.show_version()

    # devices: list[DeviceABC] = [
    #     Device(
    #         hostname="192.168.0.1",
    #         username="admin",
    #         password="P@ssw0rd",
    #         platform=Platform.ARISTA_EOS,
    #     ),
    #     Device(
    #         hostname="192.168.0.2",
    #         username="admin",
    #         password="P@ssw0rd",
    #         platform=Platform.HUAWEI_VRP,
    #     ),
    # ]
