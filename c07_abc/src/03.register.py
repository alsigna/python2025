from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    @abstractmethod
    def platform(self): ...

    @abstractmethod
    def get_running_config(self) -> str: ...


@Device.register
class CiscoIOS:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_running_config(self) -> str:
        print("собираем show running-config с устройства")
        return ""


# Device.register(CiscoIOS)

if __name__ == "__main__":
    sw = CiscoIOS("192.168.1.1")
    print(f"{isinstance(sw, Device)=}")
    sw.get_running_config()
