from typing import Self


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


class BGP:
    def __init__(self, device: Device) -> None:
        self.device = device
        self.peers: list[Device] = []

    def add_peering(self, peer: Device) -> None:
        if peer not in self.peers:
            self.peers.append(peer)
        if self.device not in peer.bgp.peers:
            peer.bgp.peers.append(self.device)


if __name__ == "__main__":
    pe1 = Device("192.168.0.1", "64512")
    pe2 = Device("192.168.0.2", "64512")
    pe3 = Device("192.168.0.3", "64512")
    rr1 = Device("192.168.0.255", "64512")
    pe1.add_peer(rr1)
    pe1.add_peer(pe3)
    pe2.add_peer(rr1)
    pe3.add_peer(rr1)

    print(pe1.bgp.peers)
    print(pe2.bgp.peers)
    print(pe3.bgp.peers)
    print(rr1.bgp.peers)
