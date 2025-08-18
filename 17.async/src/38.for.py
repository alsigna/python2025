import asyncio
import time
from collections.abc import AsyncGenerator, Generator


def log(msg: str) -> None:
    print(f"{time.perf_counter() - t0:.3f} сек: - {msg}")


async def async_counter(num: int) -> AsyncGenerator[int]:
    for i in range(num):
        await asyncio.sleep(1)
        yield i


def counter(num: int) -> Generator[int]:
    for i in range(num):
        time.sleep(1)
        yield i


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def coro_for(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    async for item in async_counter(num):
        # for item in counter(num):
        log(f"внутри for-корутины '{num}', очередной item '{item}'")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    await asyncio.gather(
        asyncio.create_task(coro(1)),
        asyncio.create_task(coro(2)),
        asyncio.create_task(coro_for(3)),
    )


if __name__ == "__main__":
    t0 = time.perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
