from typing import Any

from scrapli import Scrapli
from scrapli.response import MultiResponse

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_commands(device: dict[str, Any], commands: list[str]) -> MultiResponse:
    with Scrapli(**device) as ssh:
        return ssh.send_commands(
            commands=commands,
            stop_on_failed=True,
        )


if __name__ == "__main__":
    try:
        result = send_commands(
            device,
            [
                "show ip arp",
                "shw ip int br",
                "show version",
            ],
        )
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
