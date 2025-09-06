from typing import ClassVar


class Counter:
    # count = 0
    count: ClassVar[int] = 0
    name: str

    def __init__(self, name: str):
        self.name = name
        Counter.count += 1

    @classmethod
    def show_count(cls) -> int:
        return cls.count


c1 = Counter("First")
c2 = Counter("Second")
# c2.count = 42  # назначение ClassVar через instance считается ошибкой

print(f"{Counter.count=}")
print(f"{c1.count=}")
print(f"{c1.show_count()=}")
print(f"{c2.count=}")
print(f"{c2.show_count()=}")

c3 = Counter("Third")
print(f"{c1.count=}")
print(f"{c2.count=}")
print(f"{c3.count=}")
