from typing import Any

from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def ping_interactive(device: dict[str, Any], target: str) -> Response:
    with Scrapli(**device) as ssh:
        prompt = ssh.get_prompt()
        return ssh.send_interactive(
            interact_events=[
                ("ping", "[ip]:", False),
                ("ip", "Target IP address:", False),
                (target, "Repeat count [5]:", False),
                ("10", "Datagram size [100]:", False),
                ("1500", "Timeout in seconds [2]:", False),
                ("1", "Extended commands [n]:", False),
                ("n", "Sweep range of sizes [n]:", False),
                ("n", prompt, False),
            ],
        )


if __name__ == "__main__":
    try:
        result = ping_interactive(device, "10.255.255.102")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
