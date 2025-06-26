from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

Callable[[str], int]


def record_calling(func: Callable[Concatenate[P], R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(self: "MyClass", *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"'{func.__name__}': start, {a=}")
        func_result = func(a, *args, **kwargs)
        print(f"'{func.__name__}': finish")
        return func_result

    return wrapper


@record_calling
def add(a: int, b: int) -> int:
    """Сумма двух целых."""
    return a + b


if __name__ == "__main__":
    result = add(1, 2)
    print(result)
