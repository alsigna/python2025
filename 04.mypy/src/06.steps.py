# poetry run mypy 04.mypy/src/06.steps.py
# poetry run mypy --strict 04.mypy/src/06.steps.py


# чистый python, динамическая типизация
def calculate_a(items):
    return sum(item["price"] for item in items)


# базовая аннотация
def calculate_b(items: list[dict]) -> int:
    return sum(item["price"] for item in items)


# строгая типизация
from dataclasses import dataclass  # noqa


@dataclass
class Item:
    price: int


def calculate_c(items: list[Item]) -> int:
    return sum(item.price for item in items)


if __name__ == "__main__":
    print(calculate_a([{"price": 1}, {"price": 2}, {"price": 3}]))
    print(calculate_b([{"price": 1}, {"price": 2}, {"price": 3}]))
    print(calculate_c([Item(1), Item(2), Item(3)]))
