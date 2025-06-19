from typing import Protocol, runtime_checkable


@runtime_checkable
class Figure(Protocol):
    name: str

    @property
    def area(self) -> int: ...

    def show_figure_info(self) -> None:
        print(f"фигура '{self.name}', c площадью '{self.area}'")

    @property
    def display_colour(self) -> str:
        return "red"


class Square:
    name = "квадрат"

    def __init__(self, side: int):
        self.side = side

    @property
    def area(self) -> int:
        return self.side**2

    def show_figure_info(self) -> None:
        print(f"фигура '{self.name}', c площадью '{self.area}'")

    @property
    def display_colour(self) -> str:
        return "black"


class Rectangle(Figure):
    name = "прямоугольник"

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    @property
    def area(self) -> int:
        return self.a * self.b


def show_info(f: Figure) -> None:
    print(f.name)


if __name__ == "__main__":
    for f in Square(3), Rectangle(2, 3):
        print("-" * 10)
        show_info(f)
        if isinstance(f, Figure):
            print(f"фигура, площадь {f.area}")
        else:
            print("не фигура")
