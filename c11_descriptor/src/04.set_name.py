from typing import Any, Self


class Integer:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> int | Self:
        if instance is None:
            return self

        value = instance.__dict__.get(self.name)
        # value = getattr(instance, self.name)
        if value is None:
            raise AttributeError(f"атрибут '{self.name}' не установлен")
        elif not isinstance(value, int):
            raise ValueError(f"значение '{self.name}' должно быть int")
        else:
            return value

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"значение '{self.name}' должно быть int")
        instance.__dict__[self.name] = value


class Person:
    age: Integer = Integer()
    height: Integer = Integer()

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
