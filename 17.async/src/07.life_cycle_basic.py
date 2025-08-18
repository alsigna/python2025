import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    task = asyncio.current_task()
    log("--- внутри задачи ---")
    log(f"done: {task.done()}")
    log(f"cancelled: {task.cancelled()}")
    log(f"state: {task._state}")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    task = asyncio.create_task(coro(3))
    log("--- после создания ---")
    log(f"done: {task.done()}")
    log(f"cancelled: {task.cancelled()}")
    log(f"state: {task._state}")

    await task
    log("--- после завершения ---")
    log(f"done: {task.done()}")
    log(f"cancelled: {task.cancelled()}")
    log(f"exception: {task.exception()}")
    log(f"state: {task._state}")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
