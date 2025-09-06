import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    # if num == 1:
    #     1 / 0
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    # # ========
    # # пример 1
    # # ========
    # async with asyncio.TaskGroup() as tg:
    #     tasks = [tg.create_task(coro(i)) for i in range(1, coro_count + 1)]

    # for task in tasks:
    #     log(task.result())

    # ========
    # пример 2
    # ========
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(coro(1)),
            task2 := tg.create_task(coro(2)),
            task3 := tg.create_task(coro(3)),
            tg.create_task(coro(4)),
        ]
        await task2
        task3.cancel()

    log("код вне блока TaskGroup")

    for task in tasks:
        try:
            log(task.result())
        except asyncio.CancelledError:
            log(f"{task.get_name()} была отменена")
        except Exception as exc:
            log(f"{task.get_name()} ошибка {exc}")
    log("выход из main")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=3))
    log("асинхронный код закончен")
