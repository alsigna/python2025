from device import Device

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
