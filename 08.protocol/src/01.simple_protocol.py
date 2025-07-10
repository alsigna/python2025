from typing import Protocol, runtime_checkable


@runtime_checkable
class Device(Protocol):
    platform: str

    def reload(self, delay: int = 0) -> None: ...


class CiscoIOSXE:
    platform = "cisco_iosxe"

    def __init__(self, ip: str) -> None:
        self.ip = ip

    def reload(self, delay: int = 0) -> None:
        if delay == 0:
            print("отправляю команду 'reload'")
        else:
            print(f"отправляю команду 'reload in {delay}'")


class HuaweiVRP:
    platform = "huawei_vrp"

    def __init__(self, ip: str) -> None:
        self.ip = ip

    def reload(self, delay: int = 0) -> None:
        if delay == 0:
            print("отправляю команду 'reboot'")
        else:
            print(f"отправляю команду 'schedule reboot delay {delay}'")


if __name__ == "__main__":
    device = CiscoIOSXE("192.168.0.1")
    print(f"{isinstance(device, Device)=}")
    device.reload(delay=30)

    device = HuaweiVRP("192.168.0.1")
    print(f"{isinstance(device, Device)=}")
    device.reload(delay=30)
