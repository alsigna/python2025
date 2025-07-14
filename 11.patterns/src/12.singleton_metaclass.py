from typing import Any


class Singleton[T](type):
    _INSTANCES: dict["Singleton[T]", T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]


class Database(metaclass=Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")


class Redis(metaclass=Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")


db1 = Database("pg://1")
redis1 = Redis("redis://1")

db2 = Database("pg://2")
redis2 = Redis("redis://2")


print(f"{db1 is db2 = }")
print(f"{db1.url = }")
print(f"{db2.url = }")

print(f"{redis1 is redis2 = }")
print(f"{redis1.url = }")
print(f"{redis2.url = }")

print(f"{redis1 is db1 = }")
