import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def waiter(event):
    log("waiter: ждет событие ...")
    await event.wait()
    log("waiter: событие произошло")


async def setter(event):
    log("setter: долгие действия...")
    await asyncio.sleep(3)
    event.set()
    log("setter: флаг события установлен")


async def main():
    event = asyncio.Event()
    waiter_1 = asyncio.create_task(waiter(event))
    waiter_2 = asyncio.create_task(waiter(event))

    setter_1 = asyncio.create_task(setter(event))
    await asyncio.gather(waiter_1, waiter_2, setter_1)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
