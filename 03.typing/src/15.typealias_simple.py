import re
from collections.abc import Iterator
from textwrap import dedent

# from typing import TypeAlias

# Address: TypeAlias = str
# Netmask: TypeAlias = str
# Secondary: TypeAlias = bool

# с py3.12
type Address = str
type Netmask = str
type Secondary = bool


def get_ip(config: str) -> Iterator[tuple[Address, Netmask, Secondary]]:
    pattern = re.compile(
        pattern=r"ip address (?P<address>\S+) (?P<netmask>\S+)(?P<secondary> secondary)?",
    )
    for m in pattern.finditer(config):
        yield (
            m.group("address"),
            m.group("netmask"),
            bool(m.group("secondary")),
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
        print(ip)
