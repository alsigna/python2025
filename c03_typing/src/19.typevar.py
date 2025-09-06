from typing import TypeVar

T = TypeVar("T", int, str)
Numeric = TypeVar("Numeric", int, float)


def concat(a: T, b: T) -> T:
    return a + b


def repeat(value_to_repeat: T, n: int) -> list[T]:
    return [value_to_repeat for _ in range(n)]


def add(a: Numeric, b: Numeric) -> Numeric:
    return a + b


if __name__ == "__main__":
    print(concat(1, 2))
    print(concat("1", "2"))

    # print(repeat(1, 2))
    # print(repeat("1", 2))

    # add(10, 20)
    # add(3.14, 2.71)
    # # тут смешивание, но python допускает это, так как может привести int к float
    # # если бы было `int, str`, то автоматическое приведение невозможно и смешивать нельзя
    # add(3.14, 2)
    # add("a", "b")
