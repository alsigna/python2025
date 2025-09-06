from collections.abc import Sequence
from typing import TypeVar, overload

# example - 1


# @overload
# def foo(a: str, b: str) -> int: ...


# @overload
# def foo(a: int, b: int) -> int: ...


# def foo(a: int | str, b: int | str) -> int:
#     if isinstance(a, int) and isinstance(b, int):
#         return a + b
#     else:
#         return int(a) + int(b)


# example - 2

T = TypeVar("T", int, str)


def _concat_seq(seq: Sequence[T]) -> T:
    result: T = seq[0]
    for elem in seq[1:]:
        result = result + elem
    return result


def _concat_two(a: T, b: T) -> T:
    return a + b


@overload
def concat(a: T, b: T) -> T: ...


@overload
def concat(a: Sequence[T]) -> T: ...


def concat(a: T | Sequence[T], b: T | None = None) -> T:
    result: T
    if isinstance(a, Sequence) and b is None:
        result = _concat_seq(a)
    elif (not isinstance(a, Sequence) or isinstance(a, str)) and b is not None:
        result = _concat_two(a, b)
    else:
        raise TypeError("Invalid arguments")
    return result


if __name__ == "__main__":
    print(concat(1, 2))
    print(concat("1", "2"))
    print(concat([1, 2, 3]))
    print(concat("1", 2))
    # pow, sum как пример
