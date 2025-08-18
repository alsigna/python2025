import asyncio
import time
from asyncio import Task
from collections.abc import Awaitable, Coroutine
from inspect import isawaitable
from time import perf_counter
from typing import Any

from uvloop import Loop


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    time.sleep(2)
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    tasks_and_coros: list[Awaitable[str]] = []
    tasks_and_coros.append(asyncio.create_task(coro(2)))
    tasks_and_coros.append(coro(2))
    for obj in tasks_and_coros:
        print("-" * 10)
        print(type(obj))
        print(isawaitable(obj))
        await obj

    coros: list[Coroutine[None, None, str]] = []
    coros.append(coro(2))
    await asyncio.gather(*coros)

    tasks: list[Task[str]] = []
    tasks.append(asyncio.create_task(coro(2)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
