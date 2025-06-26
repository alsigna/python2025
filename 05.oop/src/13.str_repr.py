class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"

    def __str__(self) -> str:
        return f"{self.ip} - {self.hostname}"


if __name__ == "__main__":
    d = Device("192.168.1.1", "rt1")
    print(repr(d))
    print(f"{d!r}")
    print(str(d))
    print(f"{d}")
