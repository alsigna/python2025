import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    if num == 2:
        log(f"ошибка в корутине '{num}'")
        raise ValueError("num = 2")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    # пример 1
    tasks = [
        coro(1),
        coro(2),
        coro(3),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    log("-" * 10)
    for result in results:
        if isinstance(result, Exception):
            log(f"Ошибка!: {str(result)}")
        else:
            log(result)

    # пример 2
    tasks = [asyncio.create_task(coro(i)) for i in range(1, coro_count + 1)]
    await asyncio.gather(*tasks, return_exceptions=True)
    log("-" * 10)
    for task in tasks:
        task_name = task.get_name()
        try:
            result = task.result()
        except asyncio.CancelledError:
            log(f"задача {task_name} отменена")
        except Exception as exc:
            log(f"ошибка {exc.__class__.__name__}: {str(exc)}")
        else:
            log(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=3))
    log("асинхронный код закончен")
