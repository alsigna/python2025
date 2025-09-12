from typing import assert_never

from .models import Vendor


def get_svi_name(vendor: Vendor, svi_id: int) -> str:
    if vendor == Vendor.CISCO:
        return f"Vlan{svi_id}"
    elif vendor == Vendor.HUAWEI:
        return f"Vlanif{svi_id}"
    elif vendor == Vendor.ARISTA:
        return f"Vlan{svi_id}"
    else:
        # assert_never(vendor)
        raise RuntimeError("not supported vendor")


if __name__ == "__main__":
    for vendor in Vendor._value2member_map_.values():
        print(get_svi_name(vendor, 100))
