from typing import Final, final

MIN_LENGTH: Final[int] = 2
MIN_NEW_LENGTH: int = 2
LIST_AS_CONSTANT: list[int] = [1, 2, 3]

# тут тайпчекер должен начать ругаться
MIN_LENGTH += 1
MIN_NEW_LENGTH += 1


@final
class A:
    def info(self) -> None:
        print("класс А")


# и тут тоже, нельзя наследоваться от final класса
class B(A):
    def info(self) -> None:
        print("класс В")
