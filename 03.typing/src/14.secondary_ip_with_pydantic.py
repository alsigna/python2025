import re
from collections.abc import Iterator
from ipaddress import IPv4Address
from textwrap import dedent

from netaddr import valid_ipv4
from pydantic import BaseModel, IPvAnyAddress, field_validator


class IP(BaseModel):
    address: IPv4Address
    netmask: str
    secondary: bool

    # @field_validator("address")
    # @classmethod
    # def check_address(cls, address: str) -> str:
    #     try:
    #         IPv4Address(address)
    #     except Exception as exc:
    #         raise ValueError(f"address is not valid {address}") from exc
    #     else:
    #         return address


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
         ip address 392.168.1.1 255.255.255.0 secondary
         load-interval 30
        """,
    )

    for ip in get_ip(config):
        print(f"{ip.address} / {ip.netmask} / {ip.secondary}")
