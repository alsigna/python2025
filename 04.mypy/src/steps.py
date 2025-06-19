# чистый python, динамическая типизация
def calculate_a(items):
    return sum(item["price"] for item in items)


# базовая аннотация
def calculate_b(items: list[dict]) -> int:
    return sum(item["price"] for item in items)


# строгая типизация
from dataclasses import dataclass


@dataclass
class Item:
    price: int


def calculate_c(items: list[Item]) -> int:
    return sum(item.price for item in items)
