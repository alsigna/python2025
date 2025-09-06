from collections.abc import Iterator
from typing import TypeVar

T = TypeVar("T", str, int)


def concat(a: T, b: T) -> T:
    return a + b


def unrange_huawei_vlans(allow_pass_vlan_line: str) -> Iterator[int]:
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
