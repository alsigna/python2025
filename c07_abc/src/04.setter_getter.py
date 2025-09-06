from abc import ABC, abstractmethod

from netaddr import IPAddress


class Device(ABC):
    def __init__(self, ip: str) -> None:
        self._ip: str
        self.ip = ip

    @property
    @abstractmethod
    def ip(self) -> str: ...

    @ip.setter
    @abstractmethod
    def ip(self, ip: str) -> None: ...


class CiscoIOS(Device):
    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self._ip = ip


if __name__ == "__main__":
    sw = CiscoIOS("192.168.1.100")
    print(f"{sw.ip=}")
