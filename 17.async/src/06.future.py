import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int, fut: asyncio.Future) -> None:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    fut.set_result(f"корутина '{num}' выполнена")


async def main() -> None:
    # future = asyncio.Future()
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    task = asyncio.create_task(coro(2, future))
    log(f"{type(task) = }")
    log(f"{type(future) = }")
    log(f"{task.done() = }")
    log(f"{future.done() = }")
    await task
    log(f"{task.done() = }")
    log(f"{future.done() = }")
    await future
    log(task.result())
    log(future.result())


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
