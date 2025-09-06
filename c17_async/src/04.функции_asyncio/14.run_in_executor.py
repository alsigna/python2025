import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


def blocking_io(num: int) -> str:
    log(f"начало блокирующей операции '{num}' в другом потоке")
    time.sleep(num)
    log(f"конец блокирующей операции '{num}' в другом потоке")
    return f"корутина '{num}' выполнена"


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main():
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=2)

    tasks = [
        asyncio.create_task(coro(1), name="task-1"),
        asyncio.create_task(coro(2), name="task-2"),
        asyncio.create_task(coro(3), name="task-3"),
        # None - глобальный executor
        # loop.run_in_executor(None, blocking_io, 4),
        # либо указываем свой созданный executor
        loop.run_in_executor(executor, blocking_io, 4),
        loop.run_in_executor(executor, blocking_io, 5),
        loop.run_in_executor(executor, blocking_io, 6),
        loop.run_in_executor(executor, blocking_io, 7),
    ]
    async for task in asyncio.as_completed(fs=tasks):
        result = await task
        log(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
