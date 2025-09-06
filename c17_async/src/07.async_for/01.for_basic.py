import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Any


def log(msg: str) -> None:
    print(f"{time.perf_counter() - t0:.3f} сек: - {msg}")


async def ticker(delay: float, to: int) -> AsyncGenerator[tuple[int, Any], Any]:
    for i in range(1, to + 1):
        yield (i, delay)
        await asyncio.sleep(delay)


async def run(delay: float) -> None:
    async for i in ticker(delay, 10):
        log(i)


async def main():
    await asyncio.gather(run(0.5), run(1))


if __name__ == "__main__":
    t0 = time.perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
