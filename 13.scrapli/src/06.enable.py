from typing import Any

from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "user",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
    "auth_secondary": "P@ssw0rd",
    # "default_desired_privilege_level": "exec",
    # "default_desired_privilege_level": "privilege_exec",
    "default_desired_privilege_level": "configuration",
}


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as ssh:
        output = ssh.send_command(command)
    return output


if __name__ == "__main__":
    try:
        result = send_command(device, "do show privilege")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
