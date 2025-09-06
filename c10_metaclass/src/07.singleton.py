from typing import Any


class Singleton[T](type):
    _INSTANCES: dict["Singleton[T]", T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]


class RedisDB(metaclass=Singleton):
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} / {self.ip}>"

    def __repr__(self) -> str:
        return self.__str__()


print("-" * 10)
r1 = RedisDB("1.2.3.4")
print(r1.ip)
print(id(r1))

print("-" * 10)
r2 = RedisDB("1.2.3.4")
print(r2.ip)
print(id(r2))

print(Singleton._INSTANCES)
