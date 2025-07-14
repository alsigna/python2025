from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, ip: str):
        self.ip = ip

    @property
    @abstractmethod
    def platform(self) -> str: ...

    @property
    @abstractmethod
    def show_version_command(self) -> str: ...


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"
    show_version_command = "show version"


class HuaweiVRP(Device):
    platform = "huawei_vrp"
    show_version_command = "display version"


class DeviceFactory:
    _PLATFORM_MAP: dict[str, type[Device]] = {
        "cisco_iosxe": CiscoIOSXE,
        "huawei_vrp": HuaweiVRP,
    }

    @classmethod
    def create(cls, ip: str, platform: str) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](ip)


if __name__ == "__main__":
    for device in (
        DeviceFactory.create("192.168.1.1", "cisco_iosxe"),
        DeviceFactory.create("192.168.1.2", "huawei_vrp"),
    ):
        print(device.ip, device.platform, device.show_version_command)
