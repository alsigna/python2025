import asyncio
from time import perf_counter


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class Room:
    def __init__(self) -> None:
        self.lock = asyncio.Lock()

    async def enter(self, name: str) -> None:
        await self.lock.acquire()
        try:
            log(f"{name} вошел в комнату")
            await asyncio.sleep(1)
        finally:
            self.lock.release()
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
