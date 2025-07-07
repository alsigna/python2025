from abc import ABCMeta, abstractmethod


class Device(metaclass=ABCMeta):
    @property
    @abstractmethod
    def platform(self): ...

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def get_running_config(self) -> str: ...


class CiscoIOS(Device):
    platform = "cisco_iosxe"

    def get_running_config(self) -> str:
        print("собираем show running-config с устройства")
        return ""


if __name__ == "__main__":
    sw = CiscoIOS("192.168.1.1")
    config = sw.get_running_config()
