from typing import Self


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip


if __name__ == "__main__":
    d1 = Device("192.168.1.1", "rt1")
    d2 = Device("192.168.1.1", "rt1")
    assert d1 == d2
