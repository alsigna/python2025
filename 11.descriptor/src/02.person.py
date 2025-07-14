from typing import Any


class Integer:
    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> int | None:
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"значение '{self.name}' должно быть int")
        instance.__dict__[self.name] = value


class Person:
    age: Integer = Integer("age")
    height: Integer = Integer("height")

    def __init__(self, age: int, height: int) -> None:
        self.age = age
        self.height = height


if __name__ == "__main__":
    p1 = Person(42, 190)
    print(f"{p1.age=}")
    print(f"{p1.height=}")

    p1.age = 40
    print(f"{p1.age=}")

    print(f"{p1.__dict__=}")
    # p.age = "сорок"

    # p2 = Person(10, 150)
    # print(f"{p2.age=}")
    # print(f"{p2.__dict__=}")
    # print(f"{p1.age=}")
    # print(f"{p1.__dict__=}")
