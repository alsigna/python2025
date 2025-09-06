class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_running_config(self) -> str:
        raise NotImplementedError("метод должен быть переопределен")


class CiscoIOS(Device): ...


if __name__ == "__main__":
    sw = CiscoIOS("192.168.1.1")
    config = sw.get_running_config()
