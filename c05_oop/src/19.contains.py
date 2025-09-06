from typing import Self


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"

    def __contains__(self, value: str) -> True:
        return value == self.ip


def check_ip(ip: str) -> None:
    if ip in device:
        print(f"{ip} принадлежит устройству '{device}'")
    else:
        print(f"{ip} НЕ принадлежит устройству '{device}'")


if __name__ == "__main__":
    device = Device("192.168.1.2", "rt2")
    for ip in ["192.168.1.2", "192.168.1.200"]:
        check_ip(ip)
