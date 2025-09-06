class LoggingMixin:
    def __init__(self, *args: str, **kwargs: str) -> None:
        print("инициализация LoggingMixin")
        super().__init__(*args, **kwargs)

    def log(self, msg: str) -> None:
        print(msg)


class TaggingMixin:
    def __init__(self, *args: str, tag: str = "", **kwargs: str) -> None:
        print("инициализация TaggingMixin")
        self.tag = tag
        # super().__init__(*args, **kwargs)


class Device(TaggingMixin, LoggingMixin):
    def __init__(self, ip: str, platform: str, *args: str, **kwargs: str) -> None:
        print("инициализация Device")
        self.ip = ip
        self.platform = platform
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    d = Device("1.2.3.4", "cisco", tag="test-device")
    d.log(f"test '{d.tag=}'")
