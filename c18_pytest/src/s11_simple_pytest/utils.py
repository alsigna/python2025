from typing import TypeVar

T = TypeVar("T", str, int)


def concat(a: T, b: T) -> T:
    return a + b
