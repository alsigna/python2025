import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    try:
        await asyncio.sleep(num)
    except asyncio.CancelledError:
        log(f"корутина '{num}' отменена")
        raise
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(timeout: int, coro_count: int) -> None:
    done, pending = await asyncio.wait(
        fs=[asyncio.create_task(coro(i), name=f"task-{i}") for i in range(1, coro_count + 1)],
        timeout=timeout,
        return_when=asyncio.ALL_COMPLETED,
    )
    log(f"{len(done) = }")
    log(f"{len(pending) = }")
    for task in done:
        log(f"{task.get_name()}, {task.result()=}")
    for task in pending:
        log(f"{task.get_name()}, {task.cancel()=}")

    # дожидаемся завершения отмененных корутин
    await asyncio.gather(*pending, return_exceptions=True)
    log("выходим из main")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(timeout=2.5, coro_count=3))
    log("асинхронный код закончен")
