import time
from unittest.mock import patch


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_version(self) -> str:
        # долгие вычисления
        time.sleep(2)
        return f"{self.ip}: original version"

    def parse_output(self, output: str) -> str:
        return f"{self.ip}: {output[::-1]}"


if __name__ == "__main__":

    def show(*devices: Device) -> None:
        for device in devices:
            output = device.parse_output("12345")
            version = device.get_version()
            print(f"{output} <|> {version}")

    print("\t\t case 1")
    device = Device("1.2.3.4")
    show(device)
    with patch.object(
        target=Device,
        attribute="get_version",
    ) as mock:
        mock.return_value = "mocked"
        show(device)
    show(device)

    # ========
    print("\t\t case 2")
    device1 = Device("1.2.3.4")
    device2 = Device("5.6.7.8")
    show(device1, device2)
    with patch.object(
        target=Device,
        attribute="get_version",
        return_value="mocked",
    ):
        show(device1, device2)
    show(device1, device2)
