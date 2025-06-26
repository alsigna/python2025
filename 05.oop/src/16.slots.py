from dataclasses import dataclass, field


class Device:
    __slots__ = ("ip", "hostname")

    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __str__(self) -> str:
        return f"{self.ip} - {self.hostname}"


@dataclass(slots=True)
class Switch:
    ip: str
    hostname: str
    # location: str = field(init=False)

    def __str__(self) -> str:
        return f"{self.ip} - {self.hostname}"


if __name__ == "__main__":
    d = Device("192.168.1.1", "rt1")
    # d.location = "msk"

    sw = Switch("192.168.1.1", "sw1")
    # sw.location = "msk"
    print(sw)
