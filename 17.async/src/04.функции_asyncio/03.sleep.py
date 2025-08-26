import asyncio
import time
from time import perf_counter

import uvloop


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


# 1. использование sleep0
# не вносит задержку, а нужен для переключения корутин

# 2. подрезка таймеров
# в стандартной реализации loop (SelectorEventLoop) используется time.monotonic()
# и время постоянно синхронизируется с системным. Поэтому в примере если блокирующий
# код занимает ~3.5c, то при возвращении управления циклу событий он актуализируют время
# и подрезает оставшееся время для asyncio.sleep(5) до 1.5с, таким образом корутины coro(5)
# и coro(6) просыпаются в ожидаемое время, даже если до этого был блокирующий код (при
# условии, что этот код длился меньше времени, чем delay корутины)
# uvloop оптимизирован для async задач и использует внутреннее время и при наличии тяжелых
# блокирующих операций, оно не подрезается после возвращения управления циклу, а актуализируется
# после очередного события (3.5+5), в этот момент uvloop понимает, что и coro(6) уже просроченный,
# группирует эти таймера в один батч и пробуждает корутины.


async def bad_coro(num: int) -> str:
    log(f"начало работы блокирующей корутины '{num}'")
    for i in range(num * 1000):
        time.sleep(1 / 1000)
        if i % 100 == 0:
            log("передаем управление в event loop")
            await asyncio.sleep(0)
            log("вернули управление из event loop")
    log(f"конец работы блокирующей корутины '{num}'")
    return f"блокирующая корутина '{num}' выполнена"


async def main() -> None:
    # tasks = [asyncio.create_task(coro(i)) for i in range(7, 4, -1)]
    # tasks = [asyncio.create_task(coro(i)) for i in range(4, 10)]
    tasks = [asyncio.create_task(coro(i)) for i in range(1, 3)]
    tasks.append(asyncio.create_task(bad_coro(3)))
    await asyncio.gather(*tasks)

    # пример с uvloop.Loop
    # await asyncio.sleep(0)
    # log("начало блокирующего кода")
    # time.sleep(3.5)
    # log("конец блокирующего кода")
    # await asyncio.gather(*tasks)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(
        main=main(),
        # loop_factory=uvloop.Loop,
    )
    log("асинхронный код закончен")
