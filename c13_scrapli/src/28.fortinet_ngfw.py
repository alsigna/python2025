import logging

from rich.logging import RichHandler
from scrapli import Scrapli

device = {
    "platform": "fortinet_ngfw",
    "host": "192.168.122.106",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


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


interface_template = """
config system interface
    edit "{name}"
        set ip {ip} {mask}
        set allowaccess ping https ssh http telnet
        set description "{description}"
    next
end
"""

if __name__ == "__main__":
    with Scrapli(**device) as ssh:
        output = ssh.send_command("show system interface port1")
        print(output.result)

        output = ssh.send_command("show")
        print(output.result)

        config = interface_template.format(
            name="port2",
            ip="10.0.0.1",
            mask="255.255.255.0",
            description="test from scrapli",
        )
        output = ssh.send_commands(config.splitlines(), stop_on_failed=True)
        print(output.result)
