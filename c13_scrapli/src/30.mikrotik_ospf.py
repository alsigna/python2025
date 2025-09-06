import logging
import os
from textwrap import dedent
from types import TracebackType
from typing import Any, Literal, Self

from jinja2 import Template
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


MY_APP_CLI_USERNAME = os.getenv("MY_APP_CLI_USERNAME")
MY_APP_CLI_PASSWORD = os.getenv("MY_APP_CLI_PASSWORD")

if MY_APP_CLI_USERNAME is None or MY_APP_CLI_PASSWORD is None:
    raise ValueError("MY_APP_CLI_USERNAME / MY_APP_CLI_PASSWORD должны быть в env")


class Device:
    def __init__(self, host: str, platform: str, transport: str = "paramiko") -> None:
        self.host = host
        self.platform = platform
        self.transport: str = transport
        self.cli: Scrapli = Scrapli(**self.scrapli)

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "auth_username": MY_APP_CLI_USERNAME,
            "auth_password": MY_APP_CLI_PASSWORD,
            "auth_strict_key": False,
            "ssh_config_file": True,
            "transport": self.transport,
            "host": self.host,
            "platform": self.platform,
        }

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False

    def open(self) -> None:
        if self.cli.isalive():
            try:
                self.cli.get_prompt()
            except Exception:
                log.warning(f"{self.host}: сессия с устройство оборвана")
        if self.cli.isalive():
            return

        try:
            self.cli.open()
        except Exception as exc:
            log.exception(
                "{}: неизвестная ошибка ошибка открытия сессии, {}: {}".format(
                    self.host,
                    exc.__class__.__name__,
                    str(exc),
                ),
            )
            raise exc
        else:
            log.debug(f"{self.host}: сессия с устройством открыта")

    def close(self) -> None:
        try:
            self.cli.close()
        except Exception as exc:
            log.warning(
                "{}: ошибка закрытия сессии, {}: {}".format(
                    self.host,
                    exc.__class__.__name__,
                    str(exc),
                ),
            )
        else:
            log.debug(f"{self.host}: сессия с устройством закрыта")


cisco_template = Template(
    source=dedent(
        """
        interface {{ name }}
         ip address {{ ip }} {{ mask }}
         ip ospf network point-to-point
         exit
        !
        router ospf 1
         network {{ ip }} 0.0.0.0 area {{ area }}
         exit
        !
        """,
    ),
    lstrip_blocks=True,
    trim_blocks=True,
)

mikrotik_template = Template(
    source=dedent(
        """
        /routing/ospf/instance/add disabled=no name=ospf-instance-1 router-id=10.255.255.107
        ;
        /routing/ospf/area/add disabled=no instance=ospf-instance-1 name={{ area }}
        ;
        /routing/ospf/interface-template/add area={{ area }} disabled=no interfaces={{ name }} type=ptp
        ;
        /ip/address/add address={{ ip }}/{{ mask }} interface={{ name }}
        """,
    ),
    lstrip_blocks=True,
    trim_blocks=True,
)

if __name__ == "__main__":
    # cisco
    device = Device("192.168.122.101", "cisco_iosxe")
    config: str = cisco_template.render(
        name="GigabitEthernet4",
        ip="192.168.17.1",
        mask="255.255.255.252",
        area="0.0.0.0",
    )
    with device:
        output = device.cli.send_configs(config.splitlines(), stop_on_failed=True)

    # mikrotik
    device = Device("192.168.122.107", "mikrotik_routeros")
    config: str = mikrotik_template.render(
        name="ether2",
        ip="192.168.17.2",
        mask="255.255.255.252",
        area="0.0.0.0",
    )
    with device:
        output = device.cli.send_commands(config.splitlines(), stop_on_failed=True)
