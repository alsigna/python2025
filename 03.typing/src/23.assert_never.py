from enum import StrEnum, auto
from typing import assert_never


class Vendor(StrEnum):
    CISCO = auto()
    HUAWEI = auto()
    ARISTA = auto()
    ELTEX = auto()


def lag_name(vendor: Vendor, intf_id: int) -> str:
    # # вариант с if
    # if vendor == Vendor.CISCO:
    #     return f"Port-Channel{intf_id}"
    # elif vendor == Vendor.HUAWEI:
    #     return f"Eth-Trunk{intf_id}"
    # elif vendor == Vendor.ARISTA:
    #     return f"Port-Channel{intf_id}"
    # # elif vendor == Vendor.ELTEX:
    # #     return f"Port-Channel{intf_id}"
    # else:
    #     # assert_never(vendor)
    #     raise NotImplementedError(vendor)

    # # вариант с match
    # match vendor:
    #     case Vendor.CISCO:
    #         return f"Port-Channel{intf_id}"
    #     case Vendor.HUAWEI:
    #         return f"Eth-Trunk{intf_id}"
    #     case Vendor.ARISTA:
    #         return f"Port-Channel{intf_id}"
    #     case _:
    #         assert_never(vendor)
    #         raise NotImplementedError(vendor)

    # # вариант с dict
    # vendor_map = {
    #     Vendor.CISCO: "Port-Channel{}",
    #     Vendor.HUAWEI: "Eth-Trunk{}",
    #     Vendor.ARISTA: "Port-Channel{}",
    #     Vendor.ELTEX: "Port-Channel{}",
    # }

    # if vendor not in vendor_map:
    #     assert_never(vendor)
    #     raise NotImplementedError(vendor)
    # return vendor_map[vendor].format(intf_id)


if __name__ == "__main__":
    print(lag_name(Vendor.HUAWEI, 3))
    print(lag_name(Vendor.ELTEX, 3))
