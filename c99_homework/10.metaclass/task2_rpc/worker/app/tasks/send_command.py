import os

from scrapli import Scrapli
from scrapli.response import Response

_scrapli_template = {
    "auth_username": os.getenv("SSH_USERNAME"),
    "auth_password": os.getenv("SSH_PASSWORD"),
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostkeyAlgorithms=+ssh-rsa",
        ],
    },
}


def send_command(platform: str, host: str, command: str) -> Response:
    scrapli = _scrapli_template | {"host": host, "platform": platform}
    with Scrapli(**scrapli) as cli:  # type: ignore [arg-type]
        result = cli.send_command(command)
    return result
