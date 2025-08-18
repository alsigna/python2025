import asyncio
import time
from time import perf_counter

import uvloop


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    time.sleep(1)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    tasks = [asyncio.create_task(coro(i)) for i in range(1, 4)]
    asyncio.create_task(coro(6))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(
        main=main(),
        debug=False,
        loop_factory=uvloop.Loop,
    )
    log("асинхронный код закончен")
    log("-" * 10)

    t0 = perf_counter()
    asyncio.run(
        main=main(),
        debug=False,
        loop_factory=uvloop.Loop,
    )
    log("асинхронный код закончен")
