from collections.abc import Iterator
from enum import StrEnum, auto


class Vendor(StrEnum):
    CISCO = auto()
    HUAWEI = auto()


def unrange_huawei_vlans(allow_pass_vlan_line: str) -> Iterator[int]:
    # port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50
    vlans = allow_pass_vlan_line.split("allow-pass vlan")[1].split()
    pointer = 0
    while pointer < len(vlans):
        start = vlans[pointer]
        end = vlans[pointer]
        pointer += 1
        if pointer < len(vlans) and vlans[pointer] == "to":
            end = vlans[pointer + 1]
            pointer += 2
        yield from range(int(start), int(end) + 1)


def unrange_cisco_vlans(port_trunk_allow_pass_line: str) -> Iterator[int]:
    # switchport trunk allowed vlan 34,35,37-40,45-50
    vlans = port_trunk_allow_pass_line.split("allowed vlan")[1].split(",")
    for vlan in vlans:
        if vlan.strip().isdigit():
            yield int(vlan)
        elif "-" in vlan:
            start, end = vlan.split("-")
            yield from range(int(start), int(end) + 1)


def unrange_vlans(vendor: Vendor, line: str) -> Iterator[int]:
    if vendor == Vendor.CISCO:
        yield from unrange_cisco_vlans(line)
    elif vendor == Vendor.HUAWEI:
        yield from unrange_huawei_vlans(line)
