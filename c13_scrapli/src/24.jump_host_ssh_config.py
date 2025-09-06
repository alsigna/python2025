import logging
from typing import Any

from rich.logging import RichHandler
from scrapli import Scrapli
from scrapli.response import Response

log = logging.getLogger("scrapli")
log.setLevel(logging.DEBUG)


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


device = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "system",
    "ssh_config_file": "/Users/alexigna/projects/python2025/13.scrapli/src/ssh_scrapli_jump_host",
}


def send_command(device: dict[str, Any], command: str) -> Response:
    with Scrapli(**device) as ssh:
        return ssh.send_command(command)


if __name__ == "__main__":
    host = "192.168.122.101"
    command = "show users"
    try:
        result = send_command(
            device=device | {"host": host, "platform": "cisco_iosxe"},
            command=command,
        )
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
