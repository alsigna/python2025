# poetry run mypy 04.mypy/src/05.warn-unreachable.py
# poetry run mypy 04.mypy/src/05.warn-unreachable.py --warn-unreachable


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
        # на строку не ругается, с warn-unreachable - ошибку выдает
        print(f"unknown vendor: '{v}'")


if __name__ == "__main__":
    print(vendor_check(Vendor.CISCO))
