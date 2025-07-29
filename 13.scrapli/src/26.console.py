import logging
import time

from rich.logging import RichHandler
from scrapli import Scrapli
from scrapli.exceptions import ScrapliAuthenticationFailed
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


def login(ssh: Scrapli) -> None:
    ssh.channel.send_input_and_read(
        channel_input=ssh.auth_username,
        expected_outputs=[
            "Password:",
        ],
    )

    ssh.channel.write(channel_input=ssh.auth_password, redacted=True)
    _, output = ssh.channel.send_input_and_read(
        channel_input=ssh.comms_return_char,
        expected_outputs=[
            "% Authentication failed",
            ssh.comms_prompt_pattern,
        ],
    )
    if "% Authentication failed" in output.decode():
        raise ScrapliAuthenticationFailed("incorrect login/password")


def on_open(ssh: Scrapli) -> None:
    time.sleep(0.5)
    _, output = ssh.channel.send_input_and_read(
        channel_input=ssh.comms_return_char,
        expected_outputs=[
            "Username:",
            "Password:",
            ssh.comms_prompt_pattern,
        ],
    )
    output = output.decode()
    print(f"{output}")
    if "Password:" in output:
        ssh.channel.send_return()
        login(ssh)
    elif "Username:" in output:
        login(ssh)
    elif "Press RETURN to get started." in output:
        ssh.channel.write(ssh.comms_return_char)
        login(ssh)
    ssh.acquire_priv("privilege_exec")


def collect_via_console(host: str, port: int, command: str) -> Response:
    device = {
        "host": host,
        "port": port,
        "platform": "cisco_iosxe",
        "auth_username": "admin",
        "auth_password": "P@ssw0rd",
        "auth_strict_key": False,
        "ssh_config_file": False,
        "transport": "telnet",
        "auth_bypass": True,
        "comms_return_char": "\r\n",
        "on_open": on_open,
    }
    with Scrapli(**device) as cli:
        return cli.send_command(command)


if __name__ == "__main__":
    host = "192.168.122.1"
    port = 32769
    command = "show users"
    try:
        result = collect_via_console(host, port, command)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
