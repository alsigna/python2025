from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from device import Device
else:
    # pass
    type Device = object


class BGP:
    def __init__(self, device: Device) -> None:
        self.device = device
        self.peers: list[Device] = []

    def add_peering(self, peer: Device) -> None:
        if peer not in self.peers:
            self.peers.append(peer)
        if self.device not in peer.bgp.peers:
            peer.bgp.peers.append(self.device)
