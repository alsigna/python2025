import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    task = asyncio.create_task(coro(3))
    shielded_task = asyncio.shield(task)
    await asyncio.sleep(1)
    shielded_task.cancel()
    try:
        await shielded_task
    except asyncio.exceptions.CancelledError:
        log("попытка отмена задачи")
        await task

    log(f"{task.done()=}")
    log(f"{task.cancelled()=}")
    log(f"{task.result()=}")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
