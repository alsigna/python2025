from itertools import product
from typing import Any

from scrapli import Scrapli
from scrapli.response import Response

hosts = [
    "192.168.122.101",
    "192.168.122.102",
]

transports = [
    "system",
    # "ssh2",
    "paramiko",
    "telnet",
]

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as ssh:
        return ssh.send_command(command)


if __name__ == "__main__":
    for transport, host in product(transports, hosts):
        print("\n<<<" + "=" * 100 + ">>>")
        print(f"{host=}, {transport=}")
        try:
            result = send_command(
                device=scrapli_template | {"host": host, "transport": transport},
                command="show ip arp",
            )
        except Exception as exc:
            print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
        else:
            print(result.result)
