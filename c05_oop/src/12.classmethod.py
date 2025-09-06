from textwrap import dedent
from typing import Iterator


class ConfigParser:
    JUNK_LINES = ["!", "exit-address-family"]

    @classmethod
    def get_config(cls, config: str) -> Iterator[str]:
        for line in config.strip().splitlines():
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line

    @classmethod
    def get_patch(cls, config: str) -> Iterator[str]:
        last_space = 0
        for line in config.strip().splitlines():
            current_space = len(line) - len(line.lstrip())
            if current_space < last_space:
                last_space = current_space
                yield "exit"
            last_space = current_space
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line.strip()


if __name__ == "__main__":
    config = dedent(
        """
        ip forward-protocol nd
        no ip http server
        !
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         no shutdown
        !
        router bgp 64512
         bgp router-id 192.168.1.1
         bgp log-neighbor-changes
         !
         address-family ipv4
          redistribute connected route-map LAN
         exit-address-family
         !
         address-family vpnv4 unicast
          neighbor 1.2.3.4 activate
         exit-address-family
        !
        line vty 0 4
         password cisco
        !
        """,
    ).strip()

    for line in ConfigParser.get_patch(config):
        print(line)
