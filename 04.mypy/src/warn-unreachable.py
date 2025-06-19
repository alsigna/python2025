from enum import StrEnum, auto


class Vendor(StrEnum):
    CISCO = auto()
    HUAWEI = auto()


def vendor_check(v: Vendor) -> bool:
    if v == Vendor.CISCO:
        return True
    elif v == Vendor.HUAWEI:
        return False
    else:
        print(f"unknown vendor: '{v}'")
        # на raise не ругается
        # raise ValueError(v)


if __name__ == "__main__":
    print(vendor_check(Vendor.CISCO))
