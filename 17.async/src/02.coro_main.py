import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> str:
    for i in range(1, 6):
        await coro(i)
    return "все корутины выполнены"


if __name__ == "__main__":
    t0 = perf_counter()
    result = asyncio.run(main())
    log("асинхронный код закончен")
    print(f"{result=}")
