import asyncio
import time
from time import perf_counter
from types import TracebackType
from typing import Literal, Self


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


# Вариант 1: нет долгих блокирующих операций - оба контекстных менеджера дают одинаковый эффект:
class SyncAsyncContextManagerV1:
    def __enter__(self) -> Self:
        log("вход в sync контекст")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из sync контекста")
        return False

    async def __aenter__(self) -> Self:
        log("вход в async контекст")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из async контекста")
        return False


# Вариант 2: есть долгие блокирующие CPU-bound вычисления - оба контекстных менеджера дают одинаковый эффект:
class SyncAsyncContextManagerV2:
    OPS_COUNT = 100_000_000

    def __enter__(self) -> Self:
        for i in range(self.OPS_COUNT):
            _ = i * i % 12345
        log("вход в sync контекст")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из sync контекста")
        return False

    async def __aenter__(self) -> Self:
        for i in range(self.OPS_COUNT):
            _ = i * i % 12345
            # if i % 1_000_000 == 0:
            #     await asyncio.sleep(0)
        log("вход в async контекст")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из async контекста")
        return False


# Вариант 3: есть долгие IO-bound операции, которые можно реализовать как корутины и использовать await
# (например установление сессии с устройством, получение информации через API и пр).
class SyncAsyncContextManagerV3:
    def open(self) -> None:
        time.sleep(5)

    async def aopen(self) -> None:
        await asyncio.sleep(5)

    def __enter__(self) -> Self:
        self.open()
        log("вход в sync контекст")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из sync контекста")
        return False

    async def __aenter__(self) -> Self:
        await self.aopen()
        log("вход в async контекст")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        log("выход из async контекста")
        return False


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def coro_with(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    async with SyncAsyncContextManagerV3():
        log(f"внутри контекста корутины '{num}'")
        await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


async def main() -> None:
    await asyncio.gather(
        asyncio.create_task(coro(1)),
        asyncio.create_task(coro(2)),
        asyncio.create_task(coro_with(3)),
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("асинхронный код закончен")
