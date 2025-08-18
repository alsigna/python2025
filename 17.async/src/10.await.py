import asyncio
from asyncio import Task
from collections.abc import Awaitable, Coroutine
from inspect import isawaitable
from time import perf_counter
from typing import Any, Iterator


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class MyAwaitable:
    def __init__(self, delay: int, result: str) -> None:
        self.delay = delay
        self.result = result

    def __await__(self) -> Iterator[str]:
        log(f"начало работы __await__ с {self.delay=}")
        yield from asyncio.sleep(self.delay).__await__()
        log(f"конец работы __await__ с {self.delay=}")
        return self.result


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    result = await coro(2)
    log(result)

    result = await MyAwaitable(2, "работа собственного класса")
    log(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
