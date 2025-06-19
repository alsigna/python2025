from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def record_calling(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"'{func.__name__}': start")
        func_result = func(*args, **kwargs)
        print(f"'{func.__name__}': finish")
        return func_result

    return wrapper


@record_calling
def add(a: int, b: int) -> int:
    """Сумма двух целых."""
    return a + b


if __name__ == "__main__":
    add(1, 2)
