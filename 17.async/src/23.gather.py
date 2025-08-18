import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    if num == 2:
        log(f"ошибка в корутине '{num}'")
        raise ValueError("num = 2")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    tasks = [asyncio.create_task(coro(i)) for i in range(1, coro_count + 1)]
    # await asyncio.gather(*tasks)
    result = await asyncio.gather(*tasks, return_exceptions=True)
    log(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=3))
    log("асинхронный код закончен")
