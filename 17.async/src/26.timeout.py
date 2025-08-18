import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


def print_info(tasks: list[asyncio.Task]) -> None:
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


async def main(coro_count: int) -> None:
    # # basic
    # tasks = [asyncio.create_task(coro(i)) for i in range(1, coro_count + 1)]
    # try:
    #     async with asyncio.timeout(2.5):
    #         await asyncio.gather(*tasks, return_exceptions=True)
    # except TimeoutError:
    #     log("таймаут выполнения задач")

    # # reschedule
    # tasks = [asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)]
    # try:
    #     async with asyncio.timeout(1.5) as timeout:
    #         await tasks[0]
    #         timeout.reschedule(asyncio.get_running_loop().time() + 1)
    #         await asyncio.gather(*tasks, return_exceptions=True)
    # except TimeoutError:
    #     log("таймаут выполнения задач")

    # # cancel
    # tasks = [asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)]
    # try:
    #     async with asyncio.timeout(1.5) as timeout:
    #         await tasks[0]
    #         timeout.reschedule(None)
    #         await asyncio.gather(*tasks, return_exceptions=True)
    # except TimeoutError:
    #     log("таймаут выполнения задач")

    # remain
    tasks = [asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)]
    try:
        async with asyncio.timeout(1.5) as timeout:
            await asyncio.sleep(0.5)
            log(f"осталось {timeout.when() - asyncio.get_running_loop().time():.4f} сек")
            await asyncio.sleep(0.5)
            log(f"осталось {timeout.when() - asyncio.get_running_loop().time():.4f} сек")
            await asyncio.gather(*tasks, return_exceptions=True)
    except TimeoutError:
        log("таймаут выполнения задач")

    print_info(tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(coro_count=3))
    log("асинхронный код закончен")
