import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    await asyncio.gather(
        coro(1),
        coro(2),
        coro(3),
    )
    log("-" * 10)
    # await asyncio.gather(*[coro(i) for i in range(1, 4)])
    # print("---")
    tasks = [asyncio.create_task(coro(i)) for i in range(1, 4)]
    # step1
    await asyncio.sleep(2)
    log("main снова в работе")
    # step2
    await asyncio.gather(*tasks)
    log("все таски завершены")


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
