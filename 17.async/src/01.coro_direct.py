import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> None:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(coro(4))
    log("асинхронный код закончен")
