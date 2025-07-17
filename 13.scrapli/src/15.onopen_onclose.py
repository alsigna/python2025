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


def write_memory(ssh: Scrapli) -> None:
    ssh.send_command("write memory")


def enable_timestamp(ssh: Scrapli) -> None:
    ssh.send_command("terminal exec prompt timestamp")
    ssh.send_command("terminal length 0")


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(
        **device,
        on_open=enable_timestamp,
        on_close=write_memory,
    ) as ssh:
        output = ssh.send_command(command)
        return output


if __name__ == "__main__":
    try:
        result = send_command(device, "show ip arp")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
