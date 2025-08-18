import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    await asyncio.gather(*[coro(i) for i in range(1, coro_count + 1)])


if __name__ == "__main__":
    t0 = perf_counter()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main(coro_count=3))
    finally:
        loop.close()
    log("асинхронный код закончен")
