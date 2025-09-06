import logging
from typing import Any

from rich.logging import RichHandler
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


log = logging.getLogger("scrapli")
log.setLevel(logging.DEBUG)

# sh = logging.StreamHandler()
# log.addHandler(sh)


rh = RichHandler(
    markup=True,
    show_path=False,
    omit_repeated_times=True,
    rich_tracebacks=True,
)
rh.setFormatter(
    logging.Formatter(
        fmt="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
log.addHandler(rh)


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as ssh:
        return ssh.send_command(command=command)


if __name__ == "__main__":
    try:
        result = send_command(device, "show ver")
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
