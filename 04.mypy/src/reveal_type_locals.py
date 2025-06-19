from typing import Sequence, TypeVar

# from typing import reveal_type

type Response = dict[str, str]


def foo(a: Response, b: int) -> str:
    reveal_locals()
    reveal_type(a)
    return a["value"][::-1] * b


T = TypeVar("T")


def get_first(seq: Sequence[T]) -> T:
    reveal_type(seq[0])
    return seq[0]


if __name__ == "__main__":
    print(foo({"value": "123"}, 2))
