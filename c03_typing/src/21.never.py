from typing import Never


def never_call(arg: Never) -> None: ...


def to_int(a: int | float) -> int:
    match a:
        case int():
            return a
        case float():
            return int(round(a, 0))
        case _:
            never_call(a)
            raise ValueError("ошибка")


if __name__ == "__main__":
    print(to_int(3))
    print(to_int(3.14))
    print(to_int(3.5))
    print(to_int("3.5"))
