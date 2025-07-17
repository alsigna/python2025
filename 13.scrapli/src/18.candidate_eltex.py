import logging
from typing import Any

from rich.logging import RichHandler
from scrapli import Scrapli
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
    "platform": "eltex_esr",
    "host": "192.168.122.105",
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
    with Scrapli(**device) as ssh:
        ssh.comms_prompt_pattern = ssh.comms_prompt_pattern.replace(
            r"^(\\n)?",
            r"^(\\n|\x07)?",
        )
        output = ssh.send_configs(
            configs=configs,
            stop_on_failed=True,
        )
        if dry_run or output.failed:
            output.extend(
                ssh.send_commands(
                    commands=["show configuration changes", "", "rollback"],
                ),
            )
        else:
            output.extend(
                ssh.send_commands(
                    commands=["commit", "confirm"],
                ),
            )
        return output


if __name__ == "__main__":
    config = [
        "int loopback1",
        "description test",
    ]
    try:
        result = send_configs(device, config, False)
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        print(result.result)
