class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"


class DataCenter:
    devices = []


if __name__ == "__main__":
    d = Device("192.168.1.1", "rt1")

    print(Device.__dict__)
    print(d.__dict__)

    dc1 = DataCenter()
    dc2 = DataCenter()

    print("до добавления:")
    print(f"{dc1.devices=}")
    print(f"{dc2.devices=}")

    dc1.devices.append("r1")
    dc1.devices.append("r2")

    print("после добавления")
    print(f"{dc1.devices=}")
    print(f"{dc2.devices=}")
