import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int, fut: asyncio.Future) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    msg = f"корутина '{num}' выполнена"
    fut.set_result(msg)
    return msg


async def main() -> None:
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    task = asyncio.create_task(coro(2, future))
    log(f"{type(task) = }")
    log(f"{type(future) = }")
    log(f"{task.done() = }")
    log(f"{future.done() = }")
    # await task
    await future
    log(f"{task.done() = }")
    log(f"{future.done() = }")
    log(f"{task.result() = }")
    log(f"{future.result() = }")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
