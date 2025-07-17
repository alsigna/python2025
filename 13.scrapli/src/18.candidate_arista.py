import logging
from typing import Any

from rich.logging import RichHandler
from scrapli.driver.core import EOSDriver
from scrapli.response import MultiResponse

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
    "host": "192.168.122.104",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_configs(
    device: dict[str, Any],
    configs: list[str],
    dry_run: bool = True,
) -> MultiResponse:
    with EOSDriver(**device) as ssh:
        privilege_level = "candidate"
        ssh.register_configuration_session(session_name=privilege_level)
        output = ssh.send_configs(
            configs=configs,
            stop_on_failed=True,
            privilege_level=privilege_level,
        )
        if dry_run or output.failed:
            output.extend(
                ssh.send_configs(
                    configs=["show session-config diffs", "", "abort"],
                    privilege_level=privilege_level,
                ),
            )
        else:
            output.append(
                ssh.send_config(
                    config="commit",
                    privilege_level=privilege_level,
                ),
            )
            output.append(
                ssh.send_command(
                    command=f"no configure session {privilege_level}",
                ),
            )
        return output


if __name__ == "__main__":
    config = [
        "int loo1001",
        "description test",
        "ip address 100.64.72.201 255.255.255.255",
    ]
    try:
        result = send_configs(device, config, True)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
