import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    if num == 2:
        log(f"ошибка в корутине '{num}'")
        # ошибка в корутине прокидывается на самый верх
        # если её не отловить в try, то это приведет к закрытию цикла
        raise ValueError("num = 2")
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    tasks = [asyncio.create_task(coro(i)) for i in range(1, 4)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
