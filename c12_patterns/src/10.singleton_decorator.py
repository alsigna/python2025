from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


# def singleton(cls: type[T]) -> Callable[P, T]:
#     instances: dict[type[T], T] = {}

#     def get_instance(*args: P.args, **kwargs: P.kwargs) -> T:
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]

#     return get_instance


def singleton(cls: type[T]) -> Callable[P, T]:
    instance: T | None = None

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class Database:
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")


@singleton
class Redis:
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")


db1 = Database("pg://1")
redis1 = Redis("redis://1")
db2 = Database("pg://2")
redis2 = Redis("redis://2")


if __name__ == "__main__":
    print(f"{db1 is db2 = }")
    print(f"{db1.url = }")
    print(f"{db2.url = }")

    print(f"{redis1 is redis2 = }")
    print(f"{redis1.url = }")
    print(f"{redis2.url = }")

    print(f"{redis1 is db1 = }")  # type: ignore [comparison-overlap]
