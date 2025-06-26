from types import TracebackType
from typing import Literal, Self, Type


class RedisPool:
    def __init__(self) -> None:
        self._session: str | None = None

    def connect(self) -> None:
        if self._session is not None:
            print("сессия уже установлена")
            return
        print("сессия отсутствует, нужно создать")
        self._session = "some redis session"
        raise RuntimeError("ошибка во время открытия сессии")

    def disconnect(self):
        print("закрываем сессию")
        self._session = None

    def get_data(self) -> int:
        if self._session is None:
            raise RuntimeError("нет активной сессии")
        return 42

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        print(f"{exc_type=}")
        print(f"{exc_val=}")
        print(f"{exc_tb=}")
        self.disconnect()
        return False


if __name__ == "__main__":
    print("-" * 10, "тест 1")
    try:
        with RedisPool() as r:
            data = r.get_data()
    except Exception as exc:
        print(f"ERROR: '{exc.__class__.__name__}' - '{exc}'")
    else:
        print("данные собраны без ошибок")
        print(f"{data=}")

    print("-" * 10, "тест 2")
    try:
        with RedisPool() as r:
            data = r.get_data()
            raise ValueError("какой-то сбой")
    except Exception as exc:
        print(f"ERROR: '{exc.__class__.__name__}' - '{exc}'")
    else:
        print("данные собраны без ошибок")
        print(f"{data=}")

    print("-" * 10, "тест 3")
