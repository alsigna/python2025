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
    log(f"начало работы корутины '{num}'")
    try:
        await asyncio.sleep(num)
    except asyncio.CancelledError:
        pass
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main(timeout: int) -> None:
    try:
        # result = await asyncio.wait_for(coro(3), timeout)
        result = await asyncio.wait_for(coro_shielded(3), timeout)
    except TimeoutError:
        log(f"корутина не успела завершится за {timeout} секунд")
    else:
        log(f"корутина отработала меньше чем за {timeout} секунд")
        log(result)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main(1))
    log("асинхронный код закончен")
