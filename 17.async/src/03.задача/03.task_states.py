import asyncio
import time
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    try:
        await asyncio.sleep(num)
    except asyncio.CancelledError:
        log(f"отмена корутины '{num}'")
        raise
    if num == 2 or num == 5:
        log(f"ошибка в корутине '{num}'")
        raise ZeroDivisionError("деление на ноль")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    tasks = [asyncio.create_task(coro(i), name=f"coro-{i}") for i in range(1, 6)]
    # async for task in asyncio.as_completed(tasks):
    #     if task.get_name() == "coro-2":
    #         log("отменяем последние две задачи")
    #         tasks[-1].cancel("лишняя задача")
    #         tasks[-2].cancel("и это тоже лишняя задача")
    #     log("-" * 10)
    #     log(f"   {task.get_name()=}")
    #     log(f"   {task.done()=}")
    #     log(f"   {task.cancelled()=}")
    #     if task.cancelled():
    #         log("   задача отменена")
    #         try:
    #             # log(f"   {task.result()=}")
    #             log(f"   {task.exception()=}")
    #         except asyncio.CancelledError as exc:
    #             log(f"   {str(exc)}")
    #     else:
    #         log("   задача завершена")
    #         log(f"   {task.exception()=}")
    #         try:
    #             result = task.result()
    #             # result = await task
    #             log(f"   {result=}")
    #             # или так, для завершенной задачи `await task` тоже самое, что и `task.result()`
    #             # log(f"   {task.result()=}")
    #         except Exception as exc:
    #             log(f"   задача завершена с исключением: {str(exc)}")
    #         else:
    #             log("   задача завершена корректно без исключений")
    #         # либо получить exception и сравнивать его с None
    #         # exc = task.exception()
    #         # if exc is None:
    #         #     log("   задача завершена корректно без исключений")
    #         #     log(f"   {task.exception()=}")
    #         #     log(f"   {task.result()=}")
    #         # else:
    #         #     log("   задача завершена с исключением")
    #         #     log(f"   {task.exception()=}")

    # # краткая форма
    # async for task in asyncio.as_completed(tasks):
    #     if task.get_name() == "coro-2":
    #         log("отменяем последние две задачи")
    #         tasks[-1].cancel("лишняя задача")
    #         tasks[-2].cancel("и это тоже лишняя задача")
    #     log("-" * 10)
    #     log(f"   {task.get_name()=}")
    #     log(f"   {task.done()=}")
    #     log(f"   {task.cancelled()=}")
    #     try:
    #         result = task.result()
    #         log(f"   {task.result()=}")
    #     except asyncio.CancelledError as exc:
    #         log("   задача отменена")
    #         log(f"   {str(exc)}")
    #     except Exception as exc:
    #         log(f"   задача завершена с исключением: {str(exc)}")
    #     else:
    #         log("   задача завершена корректно без исключений")
    #         log(f"   {result=}")

    # если добавляем timeout в as_completed, то нужен еще внешний try/except для
    # отработки TimeoutError и отмены не успевших задач
    try:
        async for task in asyncio.as_completed(fs=tasks, timeout=2.5):
            if task.get_name() == "coro-2":
                tasks[-1].cancel("лишняя задача")
                tasks[-2].cancel("и это тоже лишняя задача")
            log("-" * 10)
            log(f"   {task.get_name()=}")
            try:
                log(f"   {task.result()=}")
            except asyncio.exceptions.CancelledError as exc:
                log("   задача отменена")
                log(f"   {str(exc)}")
            except Exception as exc:
                log(f"   задача завершена с исключением: {str(exc)}")
            else:
                log("   задача завершена корректно без исключений")
    except TimeoutError as exc:
        log(f"время ожидания истекло. {exc.__class__.__name__}: {str(exc)}")
        for task in tasks:
            if task.done():
                continue
            log("-" * 10)
            log(f"   отмена задачи {task.get_name()=}")
            task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    log("выход из main")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
