from typing import Any

type T = Singleton


class Singleton:
    _instance: T | None = None

    def __new__(cls: type[T], *args: Any, **kwargs: Any) -> T:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Database(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        print(f"Подключение к {url}")


class Redis(Singleton):
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
