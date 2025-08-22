# 50.semaphore_via_queue.py - добавим прогресс бар
import asyncio
from itertools import product
from random import shuffle
from time import perf_counter

from rich.live import Live
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from scrapli import AsyncScrapli
from scrapli.response import Response

DEVICES = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.103",
    "192.168.122.104",
]
COMMANDS = [
    "show interfaces description",
    "show version",
    "show ip interface brief",
]
MAX_CONNECTIONS = 2
PROGRESS_COLUMNS = (
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
)


pairs = list(product(DEVICES, COMMANDS))
shuffle(pairs)
queue = asyncio.Queue()


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


device_scrapli = {
    "transport": "asyncssh",
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ],
    },
    "timeout_socket": 5,
    "timeout_transport": 10,
    "timeout_ops": 10,
}


class ProgressBar:
    def __init__(self, total: int):
        self._stats = Progress("{task.description}", TextColumn("{task.completed}"))
        self._stats_succeeded = self._stats.add_task("[green]завершено успешно")
        self._stats_failed = self._stats.add_task("[red]завершено с ошибкой")

        self._progress = Progress(*PROGRESS_COLUMNS)
        self._progress_total = self._progress.add_task("[yellow] прогресс сбора", total=total)

        self.footer = Table.grid()
        self.footer.add_row(self._progress)
        self.footer.add_row(self._stats)

    def update_total(self) -> None:
        self._progress.update(self._progress_total, advance=1)

    def update_succeeded(self) -> None:
        self._stats.update(self._stats_succeeded, advance=1)

    def update_failed(self) -> None:
        self._stats.update(self._stats_failed, advance=1)


async def get_output_scrapli(ip: str, cmd: str) -> Response | None:
    log(f"get_output_scrapli - {ip:>15}: ⏲ корутина для сбора '{cmd}' создана")
    device = device_scrapli | {"host": ip}
    log(f"get_output_scrapli - {ip:>15}: ⏩ сбор '{cmd}'")
    try:
        async with AsyncScrapli(**device) as ssh:
            response = await ssh.send_command(cmd)
    except Exception as exc:
        log(f"get_output_scrapli - {ip:>15}: ❌ ошибка '{exc.__class__.__name__} - {str(exc)}'")
        raise exc
    else:
        log(f"get_output_scrapli - {ip:>15}: ✅ завершено '{cmd}'")
        return response


async def worker(queue: asyncio.Queue, pb: ProgressBar) -> None:
    while True:
        ip, cmd = await queue.get()
        try:
            _ = await get_output_scrapli(ip, cmd)
        except Exception:
            pb.update_failed()
        else:
            pb.update_succeeded()
        finally:
            pb.update_total()
            queue.task_done()


async def main() -> None:
    # создаем очередь задач и наполняем её
    queue = asyncio.Queue()
    for pair in pairs:
        queue.put_nowait(pair)

    pb = ProgressBar(len(pairs))
    with Live(pb.footer, refresh_per_second=10):
        # создаем ограниченное число воркеров, раньше это было ограничение через semaphore
        workers = [asyncio.create_task(worker(queue, pb)) for _ in range(MAX_CONNECTIONS)]
        # ждем, пока вся очередь не будет разобрана
        await queue.join()

    # завершаем воркеры. это и так будет сделано по завершению main(), но правильнее - явно их закрыть
    for w in workers:
        w.cancel()

    # ждем пока воркеры будут завершены
    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    t0 = perf_counter()
    asyncio.run(main())
    log("работа кода закончена")
