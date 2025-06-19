from collections.abc import Callable


def process(
    funcs: list[Callable[[int, int], int]],
    numbers: tuple[int, int],
) -> None:
    for func in funcs:
        print(func(*numbers))


if __name__ == "__main__":
    process(
        funcs=[
            pow,
            lambda a, b: a + b,
            lambda a, b: a - b,
            lambda a, b: a // b,
            lambda a, b: a % b,
        ],
        numbers=(5, 2),
    )
