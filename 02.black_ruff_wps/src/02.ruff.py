import io  # noqa: F401
import os

from scrapli import Scrapli


def concat(a: str, b: str) -> str:
    f = "test"
    return a + b


if __name__ == "__main__":
    print(concat("11", "222"))
    print(f"hello")
