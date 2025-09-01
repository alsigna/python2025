import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def coro_shielded(num: int) -> str:
    log(f"начало работы shielded-корутины '{num}'")
    try:
        await asyncio.sleep(num)
    # экранируем CancelledError, sleep завершится, на это мы не влияем,
    # но наша корутина продолжит работу
    except asyncio.CancelledError:
        log(f"попытка отмена shielded-корутины '{num}'")
    log(f"конец работы shielded-корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(timeout: float) -> None:
    task = asyncio.create_task(coro_shielded(3))
    try:
        result = await asyncio.wait_for(task, timeout)
        # result = await asyncio.wait_for(coro_shielded(3), timeout)
    except TimeoutError:
        log(f"корутина не успела завершиться за {timeout} секунд")
    else:
        log(f"корутина отработала меньше чем за {timeout} секунд")
        log(result)

    log(f"{task.done() = }")
    log(f"{task.cancelled() = }")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(1.0))
    log("асинхронный код закончен")
