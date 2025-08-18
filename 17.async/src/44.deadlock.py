import asyncio
from time import perf_counter

key1 = asyncio.Lock()
key2 = asyncio.Lock()

keys = {key1: "key-1", key2: "key-2"}


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class Room:
    async def enter(self, name: str) -> None:
        log(f"{name} вошел в комнату")
        await asyncio.sleep(1)
        log(f"{name} вышел из комнаты")


async def enter_room(name: str, room: Room, room_keys: list[asyncio.Lock]) -> None:
    # room_keys = sorted(room_keys, key=id)
    key1 = room_keys[0]
    key2 = room_keys[1]
    log(f"{name} хочет войти")
    log(f"{name} ждет ключ {keys[key1]}")
    async with key1:
        log(f"{name} использовал ключ {keys[key1]}")
        log(f"{name} ждет ключ {keys[key2]}")
        async with key2:
            log(f"{name} использовал ключ {keys[key2]}")
            await room.enter(name)
            log(f"{name} отдал ключ {keys[key2]}")
        log(f"{name} отдал ключ {keys[key1]}")


async def main():
    room = Room()
    await asyncio.gather(
        asyncio.create_task(enter_room("Bob", room, [key1, key2])),
        asyncio.create_task(enter_room("Alex", room, [key2, key1])),
        asyncio.create_task(enter_room("Alice", room, [key1, key2])),
    )


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
