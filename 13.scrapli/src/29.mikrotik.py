import logging

from rich.logging import RichHandler
from scrapli import Scrapli

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
    "platform": "mikrotik_routeros",
    "host": "192.168.122.107",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
    "transport": "paramiko",  # на system работает плохо
}


if __name__ == "__main__":
    with Scrapli(**device) as ssh:
        prompt = ssh.get_prompt()
        print(prompt)

        output = ssh.send_command(command="/export")
        print(output.result)

        output = ssh.send_command("/interface/print")
        print(output.result)

        output = ssh.send_command("/ip/address/print")
        print(output.result)
