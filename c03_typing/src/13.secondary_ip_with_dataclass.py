import re
from collections.abc import Iterator
from dataclasses import dataclass
from textwrap import dedent


@dataclass(slots=True, frozen=True)
class IP:
    address: str
    netmask: str
    secondary: bool

    def __str__(self) -> str:
        return f"{self.address} / {self.netmask} / {self.secondary}"


def get_ip(config: str) -> Iterator[IP]:
    pattern = re.compile(
        pattern=r"ip address (?P<address>\S+) (?P<netmask>\S+)(?P<secondary> secondary)?",
    )
    for m in pattern.finditer(config):
        yield IP(
            address=m.group("address"),
            netmask=m.group("netmask"),
            secondary=bool(m.group("secondary")),
        )


if __name__ == "__main__":
    config = dedent(
        """
        interface GigabitEthernet0/1
         description test
         ip address 192.168.0.1 255.255.255.0
         ip address 192.168.1.1 255.255.255.0 secondary
         load-interval 30
        """,
    )

    for ip in get_ip(config):
        print(f"{ip.address} / {ip.netmask} / {ip.secondary}")
