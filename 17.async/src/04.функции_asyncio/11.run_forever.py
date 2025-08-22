import asyncio
from pathlib import Path
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(coro_count: int) -> None:
    await asyncio.gather(*[coro(i) for i in range(1, coro_count + 1)])
    log("все корутины завершены")


async def check_status(loop: asyncio.AbstractEventLoop) -> None:
    filename = Path("shutdown")
    while True:
        await asyncio.sleep(2)
        if filename.is_file():
            log("завершаем цикл")
            await shutdown(loop)
            return
        log("завершение цикла не требуется")


async def shutdown(loop: asyncio.AbstractEventLoop) -> None:
    tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task(loop)]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


if __name__ == "__main__":
    t0 = perf_counter()
    loop = asyncio.new_event_loop()
    try:
        loop.create_task(check_status(loop))
        loop.create_task(main(coro_count=3))
        loop.run_forever()
    except KeyboardInterrupt:
        log("Принудительная остановка")
        loop.run_until_complete(shutdown(loop))
    finally:
        loop.close()
    log("асинхронный код закончен")
