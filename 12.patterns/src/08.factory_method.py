from abc import ABC, abstractmethod


#
# объекты
#
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


#
# фабрика
#


class DeviceFactory(ABC):
    @abstractmethod
    def create(cls, ip: str) -> Device: ...


class CiscoFactory(DeviceFactory):
    def create(cls, ip: str) -> Device:
        return CiscoIOSXE(ip)


class HuaweiFactory(DeviceFactory):
    def create(cls, ip: str) -> Device:
        return HuaweiVRP(ip)


if __name__ == "__main__":
    PLATFORM_TO_FACTORY = {
        "cisco_iosxe": CiscoFactory(),
        "huawei_vrp": HuaweiFactory(),
    }
    for ip, platform in (
        ("192.168.1.1", "cisco_iosxe"),
        ("192.168.1.2", "huawei_vrp"),
    ):
        device = PLATFORM_TO_FACTORY[platform].create(ip)
        print(device.ip, device.platform, device.show_version_command)
