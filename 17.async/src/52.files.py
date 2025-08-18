import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from random import randint
from time import perf_counter

import aiofile
import aiofiles
import aiopath
from aiopath import AsyncPath
from tqdm.asyncio import tqdm_asyncio


def log(msg: str) -> None:
    log_msg = f"{perf_counter() - t0:.3f} сек: - {msg}"
    # print(log_msg)
    tqdm_asyncio.write(log_msg)


async def coro(num: int) -> str:
    log(f"начало работы корутины '{num}'")
    await asyncio.sleep(num)
    log(f"конец работы корутины '{num}'")
    return f"корутина '{num}' выполнена"


#
# блокирующее чтение
#
async def read_file_block(files: list[Path]) -> None:
    log("начало работы корутины с чтением файлов")
    with tqdm_asyncio(total=len(files), desc="Чтение файлов", colour="green", ncols=80, position=0) as pbar:
        for file in files:
            with open(file, "r") as f:
                _ = f.read()
                log(f"файл {file.name} прочитан")
                time.sleep(0.1)  # больше блокирующих задержек
                pbar.update(1)


#
# добавляем asyncio.sleep на каждой итерации
#
async def read_file_sleep(files: list[Path]) -> None:
    log("начало работы корутины с чтением файлов")
    with tqdm_asyncio(total=len(files), desc="Чтение файлов", colour="green", ncols=80, position=0) as pbar:
        for file in files:
            with open(file, "r") as f:
                await asyncio.sleep(0)
                _ = f.read()
                log(f"файл {file.name} прочитан")
                time.sleep(0.1)  # больше блокирующих задержек
                pbar.update(1)


#
# выгрузка в потоки
#
def _read_file(file: Path) -> None:
    with open(file, "r") as f:
        _ = f.read()
        # если выгрузка в процессы - то это они ничего о t0 не знают, память не шарится между процессами
        log(f"файл {file.name} прочитан")
        time.sleep(0.5)  # больше блокирующих задержек


async def read_file_thread(files: list[Path]) -> None:
    loop = asyncio.get_event_loop()
    tasks = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        for file in files:
            task = loop.run_in_executor(pool, _read_file, file)
            tasks.append(task)

        log("задачи для чтения файлов выгружены в потоки")
        await tqdm_asyncio.gather(*tasks, desc="Чтение файлов", colour="green", ncols=80)


#
# выгрузка в процессы
#
async def read_file_process(files: list[Path]) -> None:
    loop = asyncio.get_event_loop()
    tasks = []
    with ProcessPoolExecutor(max_workers=5) as pool:
        for file in files:
            task = loop.run_in_executor(pool, _read_file, file)
            tasks.append(task)

        log("задачи для чтения файлов выгружены в процессы")
        await tqdm_asyncio.gather(*tasks, desc="Чтение файлов", colour="green", ncols=80)


#
# чтение через aiofiles
#
async def _read_file_aiofiles(file: Path) -> None:
    async with aiofiles.open(file, "r") as f:
        _ = await f.read()
        log(f"файл {file.name} прочитан")


async def read_file_aiofiles(files: list[Path]) -> None:
    tasks = [asyncio.create_task(_read_file_aiofiles(file)) for file in files]
    log("tasks для чтения файлов созданы")
    await tqdm_asyncio.gather(*tasks, desc="Чтение файлов", colour="green", ncols=80)


#
# чтение через aiofile
#
async def _read_file_aiofile(file: Path) -> None:
    async with aiofiles.open(file, "r") as f:
        _ = await f.read()
        log(f"файл {file.name} прочитан")


async def read_file_aiofile(files: list[Path]) -> None:
    tasks = [asyncio.create_task(_read_file_aiofile(file)) for file in files]
    log("tasks для чтения файлов созданы")
    await tqdm_asyncio.gather(*tasks, desc="Чтение файлов", colour="green", ncols=80)


#
# чтение через aiopath
#
async def _read_file_aiopath(file: Path) -> None:
    path = AsyncPath(file)
    if await path.exists():
        _ = await path.read_text()
        log(f"файл {file.name} прочитан")


async def read_file_aiopath(files: list[Path]) -> None:
    tasks = [asyncio.create_task(_read_file_aiopath(file)) for file in files]
    log("tasks для чтения файлов созданы")
    await tqdm_asyncio.gather(*tasks, desc="Чтение файлов", colour="green", ncols=80)


async def main():
    folder = Path(Path(__file__)).parent
    files = [Path(folder, "files", f"asa_logs_{i:>02}").with_suffix(".txt") for i in range(50)]

    tasks = [
        *[asyncio.create_task(coro(i)) for i in range(1, 4)],
        asyncio.create_task(read_file_thread(files)),
    ]
    await tqdm_asyncio.gather(*tasks, desc="Общий прогресс", colour="green", ncols=80)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
