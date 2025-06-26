from collections.abc import Callable


class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    def __call__(self, x: int) -> int:
        return x * self.factor

    def __str__(self) -> str:
        return f"умножитель на {self.factor}"


if __name__ == "__main__":
    # можно аннотировать list[Multiplier] или list[Callable[[int], int]], зависит от контекста
    # funcs: list[Multiplier] = [
    funcs: list[Callable[[int], int]] = [
        Multiplier(2),
        Multiplier(3),
        lambda x: x * 4,
    ]
    num = 10
    for func in funcs:
        # print(f"{func}: {num} * {func.factor} = {func(num)}")  # тут обращение к атрибутам, поэтому Multiplier
        print(func(num))  # а тут можно более универсально: Callable
