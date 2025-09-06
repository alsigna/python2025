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
        print(device.version)

    with patch.object(
        target=Device,
        attribute="version",
        spec=True,
        return_value="mocked",
        new_callable=PropertyMock,
    ):
        print(device.version)
        print(device.ip)

    with patch.object(
        target=device,
        attribute="ip",
        new="127.0.0.1",
    ):
        print(device.ip)
    print(device.ip)
