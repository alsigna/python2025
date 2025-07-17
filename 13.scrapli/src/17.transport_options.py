from typing import Any

from pydantic import BaseModel
from scrapli import Scrapli
from scrapli.response import Response


class Device(BaseModel):
    host: str
    platform: str
    transport: str = "system"

    def __hash__(self) -> int:
        return hash(self.host + self.platform)


scrapli_template = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    # "ssh_config_file": "/Users/alexigna/projects/python2025/12.scrapli/src/ssh_scrapli",
    "ssh_config_file": True,
    # "transport_options": {
    #     "open_cmd": [
    #         "-o",
    #         "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
    #         "-o",
    #         "HostKeyAlgorithms=+ssh-rsa",
    #     ]
    # },
}

devices = {
    Device(host="192.168.122.101", platform="cisco_iosxe"): "show clock",
    Device(host="192.168.122.102", platform="cisco_iosxe"): "show clock",
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
                device=scrapli_template | device.model_dump(),
                command=command,
            )
        except Exception as exc:
            print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
        else:
            print(result.result)
