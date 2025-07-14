from abc import ABC, abstractmethod


class Device(ABC):
    @property
    @abstractmethod
    def platform(self): ...

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def get_running_config(self) -> None: ...


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"

    def get_running_config(self) -> None:
        print("собираем show running-config с устройства")


class HuaweiVRP(Device):
    platform = "huawei_vrp"

    def get_running_config(self) -> None:
        print("собираем display current-configuration с устройства")


if __name__ == "__main__":
    d1 = CiscoIOSXE("192.168.1.1")
    d1.get_running_config()
    d2 = HuaweiVRP("192.168.1.2")
    d2.get_running_config()
