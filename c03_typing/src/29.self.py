from typing import Self


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def __str__(self) -> str:
        return f"{self.name}, {self.age}"


class Admin(Person):
    def __init__(self, name: str, age: int, os: str) -> None:
        self.name = name
        self.age = age


if __name__ == "__main__":
    person = Person("user", 42).with_name("admin")
    admin = Admin("admin", 42, "ubuntu").with_name("user")
    print(person)
