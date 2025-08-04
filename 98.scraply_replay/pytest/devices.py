import re

from scrapli import Scrapli


class CiscoDevice:
    def __init__(self, host: str) -> None:
        self.cli = Scrapli(
            host=host,
            platform="cisco_iosxe",
            auth_strict_key=False,
            auth_username="admin",
            auth_password="P@ssw0rd",
            transport_options={
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        )

    def get_version(self) -> str:
        with self.cli:
            output = self.cli.send_command("show version | i Software")
        if output.failed:
            return ""

        version = re.findall(r"version ([a-z0-9_\.\(\)]*)", output.result, flags=re.I)
        if not version:
            return ""

        return version[0]


if __name__ == "__main__":
    device = CiscoDevice("192.168.122.101")
    version = device.get_version()
    print(version)
