from typing import Any


def foo(a: list[Any]) -> str:
    if len(a) != 0:
        return a[0]
    return ""


if __name__ == "__main__":
    print(foo(["1", "2"]))
