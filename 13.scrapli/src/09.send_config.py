from textwrap import dedent
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


def send_config(device: dict[str, Any], config: str) -> Response:
    with Scrapli(**device) as ssh:
        return ssh.send_config(
            config=config,
            strip_prompt=False,
            # timeout_ops=10,
            # failed_when_contains="%",
            stop_on_failed=True,
        )


if __name__ == "__main__":
    config = dedent(
        """
        int loo1001
         ip address 100.64.72.201 255.255.255.255
        int loo1002
         ip address 100.64.73.101 255.255.255.255
        """,
    )
    # config = "no ip domain lookup"
    try:
        result = send_config(device, config)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.channel_input)
        print(result.result)
