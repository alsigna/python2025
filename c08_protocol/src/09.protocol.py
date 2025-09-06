from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto
from ipaddress import IPv4Address
from typing import NewType, Protocol, Self, runtime_checkable


class Platform(StrEnum):
    CISCO_IOSXE = auto()
    ARISTA_EOS = auto()
    HUAWEI_VRP = auto()


IP = NewType("IP", str)


def check_ip(value: str) -> IP:
    try:
        IPv4Address(value)
    except Exception as exc:
        raise ValueError(f"incorrect ip: {str(exc)}") from None
    else:
        return IP(value)


@dataclass(frozen=True, slots=True)
class APIDevice:
    ip: IP
    platform: Platform

    @classmethod
    def parse(cls, ip: str, platform: str, **kwargs: str) -> Self:
        return cls(ip=check_ip(ip), platform=Platform(platform))


@dataclass(slots=True)
class APIAnswer:
    devices: list[APIDevice]

    @classmethod
    def parse(cls, data: list[dict[str, str]]) -> Self:
        device_list = [APIDevice.parse(**device) for device in data]
        return cls(devices=device_list)


@runtime_checkable
class Device(Protocol):
    platform: Platform

    def __init__(self, ip: IP): ...

    @property
    def ip(self) -> IP: ...

    @property
    def _version(self) -> str: ...

    @property
    def version(self) -> str: ...

    def update_version(self) -> None: ...

    def _extract_version(self) -> str: ...


class BaseDevice:
    def __init__(self, ip: IP):
        self.ip = ip
        self._version = ""

    @property
    def version(self) -> str:
        if len(self._version) == 0:
            self.update_version()
        return self._version

    @version.setter
    def version(self) -> None:
        raise NotImplementedError("read-only свойство")

    def update_version(self) -> None:
        self._version = self._extract_version()

    @abstractmethod
    def _extract_version(self) -> str: ...


class CiscoIOSXE(BaseDevice):
    platform = Platform.CISCO_IOSXE

    def _extract_version(self) -> str:
        return "15.2(3)M6"


class AristaEOS(BaseDevice):
    platform = Platform.ARISTA_EOS

    def _extract_version(self) -> str:
        return "4.13.2F"


class HuaweiVRP(BaseDevice):
    platform = Platform.HUAWEI_VRP

    def _extract_version(self) -> str:
        return "V100R005C60"


class DeviceFactory:
    _PLATFORM_MAP: dict[Platform, type[Device]] = {
        Platform.CISCO_IOSXE: CiscoIOSXE,
        Platform.ARISTA_EOS: AristaEOS,
        Platform.HUAWEI_VRP: HuaweiVRP,
    }

    @classmethod
    def create(cls, ip: IP, platform: Platform) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](ip)


if __name__ == "__main__":
    raw_answer = [
        {
            "ip": "192.168.0.1",
            "platform": "cisco_iosxe",
        },
        {
            "ip": "192.168.0.2",
            "platform": "arista_eos",
        },
        {
            "ip": "192.168.0.3",
            "platform": "huawei_vrp",
        },
    ]
    answer = APIAnswer.parse(raw_answer)
    for device in answer.devices:
        d = DeviceFactory.create(device.ip, device.platform)
        print(f"{isinstance(d, Device)=}")
        print(d.platform, d.version, sep="\t")
