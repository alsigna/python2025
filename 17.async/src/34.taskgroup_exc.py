import asyncio
from time import perf_counter
from typing import NoReturn


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def exc_coro(num: int) -> NoReturn:
    log(f"начало работы корутины-исключение '{num}'")
    try:
        await asyncio.sleep(num)
    except asyncio.CancelledError:
        pass
    log(f"конец работы корутины-исключение '{num}'")
    raise ValueError(f"ошибка из корутины-исключение '{num}' ")


async def main(coro_count: int) -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(coro(i), name=f"coro-{i}") for i in range(1, coro_count + 1)]
            tasks.extend(tg.create_task(exc_coro(i), name=f"exc-coro-{i}") for i in (2, 3))
    except* ValueError as gexc:
        for exc in gexc.exceptions:
            log(f"ERROR: {exc.__class__.__name__}: {str(exc)}")

    for task in tasks:
        log("-" * 10)
        log(f"name: {task.get_name()}")
        log(f"done: {task.done()}")
        log(f"cancelled: {task.cancelled()}")
        try:
            log(f"result: {task.result()}")
        except asyncio.CancelledError:
            log("result: <отсутствует, задача отменена>")
        except Exception as exc:
            log(f"result: <отсутствует, исключение {exc.__class__.__name__}: {str(exc)}>")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=3))
    log("асинхронный код закончен")
