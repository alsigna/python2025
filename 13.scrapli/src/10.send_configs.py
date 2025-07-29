from textwrap import dedent
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


def send_configs(device: dict[str, Any], configs: list[str]) -> MultiResponse:
    with Scrapli(**device) as ssh:
        return ssh.send_configs(
            configs=configs,
            stop_on_failed=True,
        )


if __name__ == "__main__":
    config = [
        "int loo101",
        "ip address 100.64.72.101 255.255.255.255",
        "int loo102",
        "ip address 100.64.73.102 255.255.255.255",
    ]
    try:
        result = send_configs(device, config)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
