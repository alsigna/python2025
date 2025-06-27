class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        print("Device init")
        self.hostname = hostname
        self.ip = ip

    def show_info(self) -> None:
        print("from Device")
        print(f"{self.hostname=}, {self.ip=}")


class Cisco:
    def __init__(self) -> None:
        print("Cisco init")
        self.vendor = "cisco"

    def show_info(self) -> None:
        print("from Cisco")
        print(f"{self.hostname=}, {self.ip=}")


class Router(Cisco, Device):
    def __init__(self, hostname: str, ip: str, platform: str) -> None:
        print("Router init")
        Cisco.__init__(self)
        Device.__init__(self, hostname, ip)
        self.platform = platform


if __name__ == "__main__":
    rt = Router("rt1", "192.168.1.1", "xe")
    print(f"{rt.ip=}")
    print(f"{rt.hostname=}")
    print(f"{rt.platform=}")
    print(f"{rt.vendor=}")
    rt.show_info()
