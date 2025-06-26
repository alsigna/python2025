# poetry run mypy 04.mypy/src/04.warn-return-any.py
# poetry run mypy 04.mypy/src/04.warn-return-any.py --warn-return-any


from typing import Any


def foo(a: list[Any]) -> str:
    if len(a) != 0:
        return a[0]
    return ""


if __name__ == "__main__":
    print(foo(["1", "2"]))
