# https://temp.pm

import asyncio
from random import randint
from time import perf_counter

import aiohttp

CACHE = {}

DEVICES = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"]
URL = "https://temp.pm/?n88AFlMzhGf0TQIWz1JOYHEEc-3-01iQAQ4z0yyYi593Wu1qd1285-N"

LOCK = asyncio.Lock()


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


async def read_temp_pm(url: str, device: str) -> str:
    await asyncio.sleep(randint(10, 50) / 100)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            text = await response.text()
            log(f"{device} - read_temp_pm: запрос из сервиса")
            if "The message has either been read/expired/deleted or this URL is invalid." in text:
                log(f"{device} - read_temp_pm: password отсутствует в сервисе")
                raise ValueError("Сообщение отсутствует.")
            message = text.split('<div class="panel-body panel-message2">')[1].split("</div>")[0]
            log(f"{device} - read_temp_pm: password получен из сервиса: {message}")
            return message.strip()


async def get_device_password(device: str) -> str:
    password = CACHE.get("password")
    if password is None:
        log(f"{device} - get_device_password: password не в кеше")
        try:
            password = await read_temp_pm(URL[:-2], device)
        except ValueError as exc:
            return f"ERROR: {str(exc)}"
        else:
            CACHE["password"] = password
    else:
        log(f"{device} - get_device_password: password уже есть в кеше")
    return password


async def get_device_password_with_lock(device: str) -> str:
    password = CACHE.get("password")
    if password is not None:
        log(f"{device} - get_device_password: password уже есть в кеше")
        return password

    log(f"{device} - get_device_password: ждем lock")
    async with LOCK:
        password = CACHE.get("password")
        if password is not None:
            log(f"{device} - get_device_password: password уже есть в кеше (повторная проверка)")
            return password
        try:
            password = await read_temp_pm(URL[:-2], device)
        except ValueError as exc:
            return f"ERROR: {str(exc)}"
        else:
            CACHE["password"] = password
            return password


async def prepare_device(device: str) -> tuple[str, str]:
    if device.endswith(("2", "4")):
        await asyncio.sleep(0.5)
    password = await get_device_password_with_lock(device)
    # password = await get_device_password(device)
    return device, password


async def main() -> None:
    tasks = [asyncio.create_task(prepare_device(device)) for device in DEVICES]
    result = await asyncio.gather(*tasks)
    for pair in result:
        log(f"{pair[0]}, {pair[1]}")
    log(CACHE)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
