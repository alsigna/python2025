import re
from types import TracebackType
from typing import Any, Literal, Self

from scrapli import Scrapli


class Device:
    def __init__(self, host: str) -> None:
        self.host = host
        self.platform = "cisco_iosxe"
        self.cli: Scrapli = Scrapli(**self.scrapli)

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "auth_username": "admin",
            "auth_password": "P@ssw0rd",
            "auth_secondary": "P@ssw0rd",
            "platform": self.platform,
            "transport": "system",
            "host": self.host,
            "auth_strict_key": False,
            "port": 22,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        }

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    def open(self) -> None:
        self.cli.open()

    def close(self) -> None:
        self.cli.close()

    def get_version(self) -> str:
        output = self.cli.send_command("show version")
        if output.failed:
            return "ERROR"
        re_version = re.search(r"Version (?P<version>\S+), ", output.result)
        return re_version.group("version")


if __name__ == "__main__":
    device = Device("192.168.122.101")
    with device:
        version = device.get_version()
        print(version)
