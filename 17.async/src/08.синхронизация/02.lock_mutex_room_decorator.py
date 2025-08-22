import asyncio
from asyncio import Lock
from collections.abc import Awaitable, Callable
from time import perf_counter
from typing import ParamSpec, TypeVar


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


P = ParamSpec("P")
R = TypeVar("R")

room_lock = asyncio.Lock()


def lock_decorator(lock: Lock) -> Callable[
    [Callable[P, Awaitable[R]]],
    Callable[P, Awaitable[R]],
]:
    """Декоратор для использования asyncio.Lock.

    Args:
        lock: экземпляр asyncio.Lock для синхронизации
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with lock:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


class Room:
    @lock_decorator(room_lock)
    async def enter(self, name: str) -> None:
        log(f"{name} вошел в комнату")
        await asyncio.sleep(1)
        log(f"{name} вышел из комнаты")


async def enter_room(name: str, room: Room) -> None:
    log(f"{name} хочет войти")
    await room.enter(name)


async def main():
    room = Room()
    await asyncio.gather(
        asyncio.create_task(enter_room("Bob", room)),
        asyncio.create_task(enter_room("Alex", room)),
        asyncio.create_task(enter_room("Alice", room)),
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
