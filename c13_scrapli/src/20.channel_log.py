from typing import Any

from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(
        **device,
        # channel_log=True,
        channel_log_mode="write",
        channel_log="./20.channel_log.log",
    ) as ssh:
        return ssh.send_command(command=command)


if __name__ == "__main__":
    try:
        result = send_command(device, "show version")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
