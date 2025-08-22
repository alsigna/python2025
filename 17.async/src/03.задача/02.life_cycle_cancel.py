import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    task = asyncio.current_task()
    log("--- внутри задачи ---")
    log(f"    done: {task.done()}")
    log(f"    cancelled: {task.cancelled()}")
    log(f"    state: {task._state}")  # noqa: SLF001
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def shielded_coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    try:
        await asyncio.sleep(num)
    except asyncio.exceptions.CancelledError:
        log(f"попытка отмена корутины '{num}'")
    task = asyncio.current_task()
    log("--- внутри задачи ---")
    log(f"    done: {task.done()}")
    log(f"    cancelled: {task.cancelled()}")
    log(f"    state: {task._state}")  # noqa: SLF001
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    # task = asyncio.create_task(shielded_coro(2))
    task = asyncio.create_task(coro(3))

    log("--- после создания ---")
    log(f"    done: {task.done()}")
    log(f"    cancelled: {task.cancelled()}")
    log(f"    state: {task._state}")  # noqa: SLF001

    # переключаемся, что бы coro(3) начала выполняться
    await asyncio.sleep(0)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    log("--- после отмены ---")
    log(f"    done: {task.done()}")
    log(f"    cancelled: {task.cancelled()}")
    log(f"    state: {task._state}")  # noqa: SLF001


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
