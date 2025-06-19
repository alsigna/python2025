from typing import Self

from bgp import BGP


class Device:
    def __init__(self, ip: str, asn: str) -> None:
        self.ip = ip
        self.asn = asn
        self.bgp = BGP(self)

    def add_peer(self, peer: Self) -> None:
        self.bgp.add_peering(peer)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.ip}, {self.asn})"

    def __repr__(self) -> str:
        return str(self)
