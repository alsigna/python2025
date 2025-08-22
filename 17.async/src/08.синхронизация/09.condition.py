# пример с condition.
# есть БД в которую автоматически пишутся данные корутинами auto_write_data, которые ждут
# уведомление о готовности данных, и как только оно получено - пишут их в БД.
# данные готовит корутина download_data, как только данные готовы, она отправляет
# condition.notify() давая возможность очередной корутине auto_write_data продолжить работу
# и записать данные. Кроме этого есть корутина manual_write_data, которая так же пишет в БД,
# но свои данные. Что бы сделать БД эксклюзивным ресурсом используется Lock. При этом для
# condition в auto_write_data/download_data и manual_write_data используется один и тот же объект
# Lock, что бы гарантировать, что доступ к БД будет эксклюзивным вне зависимости от того, кто обращается.

import asyncio
from time import perf_counter

ITEMS_COUNT = 4


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def auto_write_data(condition: asyncio.Condition, data: str) -> None:
    async with condition:
        log(f"ожидает готовности данных: '{data}'")
        await condition.wait()
        log(f"'{data}' добавляются в БД ...")
        await asyncio.sleep(1)
        log(f"'{data}' автоматически записаны в БД")


async def download_data(condition: asyncio.Condition) -> None:
    for i in range(1, ITEMS_COUNT + 1):
        async with condition:
            await asyncio.sleep(1)
            log(f"'данные для авто-записи {i}' готовы для записи в БД")
            condition.notify()


async def manual_write_data(lock: asyncio.Lock, data: str) -> None:
    await asyncio.sleep(3)
    async with lock:
        log(f"'{data}' добавляются в БД ...")
        await asyncio.sleep(1)
        log(f"'{data}' вручную записаны в БД")


async def main():
    lock = asyncio.Lock()
    condition = asyncio.Condition(lock)

    tasks = [
        asyncio.create_task(auto_write_data(condition, f"данные для авто-записи {i}"))
        for i in range(1, ITEMS_COUNT + 1)
    ]
    manual_task = asyncio.create_task(manual_write_data(lock, "данные для ручной записи"))
    await asyncio.gather(download_data(condition), *tasks, manual_task)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
