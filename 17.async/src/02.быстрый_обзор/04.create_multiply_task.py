import asyncio
from time import perf_counter, sleep


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> str:
    task1 = asyncio.create_task(coro(1))
    task2 = asyncio.create_task(coro(2))
    task3 = asyncio.create_task(coro(3))
    log("задачи созданы")
    await task3

    # await asyncio.sleep(3)
    # sleep(2)
    # await asyncio.sleep(0)
    log("выходим из main")
    return "все задачи выполнены"


if __name__ == "__main__":
    t0 = perf_counter()
    # sleep(1)
    # цикла событий еще нет
    result = asyncio.run(main())
    # цикла событий уже нет
    log("асинхронный код закончен")
    log(f"{result=}")
