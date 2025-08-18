from typing import Iterator


def foo() -> Iterator[int]:
    start = 0
    while True:
        start += 1
        yield pow(start, 2)


async def afoo() -> None:
    print(42)


if __name__ == "__main__":
    f = foo()
    print(f)

    af = afoo()
    print(af)
