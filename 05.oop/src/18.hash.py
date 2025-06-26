from typing import Self


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)


if __name__ == "__main__":
    d1 = Device("192.168.1.1", "rt1")
    d2 = Device("192.168.1.2", "rt1")

    configs = {
        d1: "config1",
        d2: "config2",
    }
