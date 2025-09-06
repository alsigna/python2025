import logging
from typing import Any

from scrapli_replay.server.collector import ScrapliCollector

log = logging.getLogger("scrapli")
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
log.addHandler(sh)


class CiscoIOSXESpec:
    channel_inputs = [
        "show version",
        "show ip int br",
        "sh ip ospf ne",
    ]
    interact_events = [
        [
            ("clear logging", "[confirm]", False),
            ("", "#", False),
        ],
    ]
    paging_indicator = "--More--"
    paging_escape_string = "\x1b"


class Device:
    PLATFORM_MAP = {
        "cisco_iosxe": CiscoIOSXESpec,
    }

    def __init__(self, ip: str, platform: str) -> None:
        self.ip = ip
        self.platform = platform
        self.spec = self.PLATFORM_MAP[platform]
        self.collector = ScrapliCollector(
            channel_inputs=self.spec.channel_inputs,
            interact_events=self.spec.interact_events,
            paging_indicator=self.spec.paging_indicator,
            paging_escape_string=self.spec.paging_escape_string,
            collector_session_filename=f"collector_session_dump_{self.ip}.yaml",
            **self.scrapli,
        )

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "host": self.ip,
            "platform": self.platform,
            "auth_username": "admin",
            "auth_password": "P@ssw0rd",
            "auth_secondary": "P@ssw0rd",
            "auth_strict_key": False,
            "timeout_ops": 120,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        }


for ip, platform in [
    ("192.168.122.101", "cisco_iosxe"),
    ("192.168.122.102", "cisco_iosxe"),
]:
    device = Device(ip, platform)
    device.collector.open()
    device.collector.collect()
    device.collector.close()
    device.collector.dump()
