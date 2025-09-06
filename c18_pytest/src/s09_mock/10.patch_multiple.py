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
            output = device.parse_output("some text")
            version = device.get_version()
            print(f"{output} <|> {version}")

    def mock_parse_output(self: Device, output: str) -> str:
        return f"{self.ip}: mocked! {output[::2]}"

    device = Device("1.2.3.4")
    show(device)
    with patch.multiple(
        target=Device,
        get_version=lambda self: f"{self.ip}: mocked!",
        parse_output=mock_parse_output,
    ):
        show(device)
    show(device)
