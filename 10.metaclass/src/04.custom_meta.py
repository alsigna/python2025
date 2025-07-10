from typing import Any


class MyMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type[Any]:
        print(f"создание класса '{name}'")
        attrs["created_by"] = "MyMeta"
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMeta):
    def __init__(self, value: str):
        self.value = value


if __name__ == "__main__":
    c = MyClass("test")
    print(c.value)
    print(c.created_by)
