from dataclasses import asdict, dataclass
from typing import Any

from scrapli import Scrapli
from scrapli.response import Response


@dataclass(slots=True)
class Device:
    host: str
    platform: str
    transport: str = "system"

    def __hash__(self) -> int:
        return hash(self.host + self.platform)


scrapli_template = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}

devices = {
    Device(host="192.168.122.101", platform="cisco_iosxe"): "show ip arp",
    Device(host="192.168.122.102", platform="cisco_iosxe", transport="telnet"): "show ip arp",
    Device(host="192.168.122.103", platform="huawei_vrp"): "display arp",
    Device(host="192.168.122.104", platform="arista_eos"): "show ip arp",
}


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as ssh:
        return ssh.send_command(command)


if __name__ == "__main__":
    for device, command in devices.items():
        print("\n<<<" + "=" * 100 + ">>>")
        print(f"{device.host=}, {command}")
        try:
            result = send_command(
                device=scrapli_template | asdict(device),
                command=command,
            )
        except Exception as exc:
            print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
        else:
            print(result.result)
