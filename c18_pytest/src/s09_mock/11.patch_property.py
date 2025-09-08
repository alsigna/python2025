from unittest.mock import MagicMock, PropertyMock, patch


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    @property
    def version(self) -> str:
        return "1.0"


if __name__ == "__main__":

    device = Device("1.2.3.4")

    # обычное мокирование не работает, т.к. version это property
    with patch.object(
        target=Device,
        attribute="version",
        spec=True,
        return_value="mocked",
    ):
        print("\n\tcase-1")
        print(device.version)
        print(device.ip)

    # нужно использовать PropertyMock
    with patch.object(
        target=Device,
        attribute="version",
        spec=True,
        return_value="mocked",
        new_callable=PropertyMock,
    ):
        print("\n\tcase-2")
        print(device.version)
        print(device.ip)

    # если меням обычный атрибут, то нужно использовать new
    with patch.object(
        target=device,
        attribute="ip",
        new="127.0.0.1",
    ):
        print("\n\tcase-3")
        print(device.version)
        print(device.ip)

    # если нужно передавать динамическое значение, и мы хотим перейти, то
    # PropertyMock c side_effect плохо работает, поэтому используем new + property
    def fake_version(self) -> str:
        return f"version of {self.ip} is 3.3.3"

    with patch.object(
        target=Device,
        attribute="version",
        spec=True,
        new=property(fake_version),
    ):
        print("\n\tcase-4")
        print(device.version)
        print(device.ip)
