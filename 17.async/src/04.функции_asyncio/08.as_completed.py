import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    try:
        await asyncio.sleep(num)
    # логируем отмену и пробрасываем наверх
    except asyncio.CancelledError:
        log(f"корутина '{num}' отменена")
        raise
    # вручную генерируем исключение
    if num == 2:
        raise ZeroDivisionError("деление на ноль!")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(timeout: int, coro_count: int) -> None:
    # вариант с AsyncIterator
    tasks = [asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)]
    try:
        async for task in asyncio.as_completed(
            fs=tasks,
            timeout=timeout,
        ):
            try:
                log(f"{task.get_name()} - {task.result()=}")
            except ZeroDivisionError as exc:
                log(f"{task.get_name()} - {str(exc)}")
    except TimeoutError:
        log("время ожидания истекло")
        for task in tasks:
            if not task.done():
                task.cancel()
    # ждем отмены опоздавших задач, можно отдельно список с ними собрать, а можно и исходный использовать
    result = await asyncio.gather(*tasks, return_exceptions=True)
    log(result)
    log("выход из main")

    # # вариант с SyncIterator
    # tasks = [asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)]
    # for task in asyncio.as_completed(
    #     fs=tasks,
    #     timeout=timeout,
    # ):
    #     try:
    #         result = await task
    #     except TimeoutError:
    #         log("timeout!!!")
    #     except ZeroDivisionError:
    #         log("деление на ноль!!!")
    #     else:
    #         log(result)
    # for task in tasks:
    #     if not task.done():
    #         task.cancel()
    # result = await asyncio.gather(*tasks, return_exceptions=True)
    # log(result)
    # log("выход из main")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(timeout=2.5, coro_count=5))
    log("асинхронный код закончен")
