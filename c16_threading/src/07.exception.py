import threading
import traceback
from collections.abc import Callable
from threading import BoundedSemaphore, Thread
from time import perf_counter
from typing import Any

from scrapli import Scrapli

max_connections = 2
pool = BoundedSemaphore(max_connections)


def log(msg: str) -> None:
    print(f"{perf_counter() - t0:.3f} сек: - {msg}")


class ThreadWithResult(Thread):
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(group, target, name, *args, **kwargs)
        self._result = None

    def run(self) -> None:
        if self._target is not None:
            self._result = self._target(*self._args, **self._kwargs)

    def join(self, *args: Any) -> Any:
        super().join(*args)
        return self._result


scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    log(f"{host:>15}: подключение...")

    if host == "192.168.122.114":
        raise ValueError("неизвестный хост")

    device = scrapli_template | {"host": host}
    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")
    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    log(f"{host:>15}: завершено")
    return result


def custom_hook(args: Any) -> None:
    exc_type, exc_value, exc_traceback, exc_thread = args
    print(f"Тип исключения: {exc_type.__name__}")
    print(f"Сообщение исключения: {exc_value}")
    print(f"Номер потока: {exc_thread.ident}")
    print(f"Имя потока: {exc_thread.name}")
    print(f"Функция потока: {exc_thread._target.__name__}")  # noqa:SLF001
    print(f"Аргументы потока: {exc_thread._args[0]}")  # noqa:SLF001

    # print("Traceback исключения:")
    # traceback.print_tb(exc_traceback)


threading.excepthook = custom_hook


def print_version_sem(host: str) -> str:
    with pool:
        return print_version(host)


if __name__ == "__main__":
    ip_addresses = [
        "192.168.122.102",
        "192.168.122.109",
        "192.168.122.110",
        "192.168.122.111",
        "192.168.122.112",
        "192.168.122.113",
        "192.168.122.114",
        "192.168.122.115",
        "192.168.122.116",
        "192.168.122.117",
        "192.168.122.101",
        "192.168.122.118",
    ]

    threads: list[Thread] = []
    t0 = perf_counter()
    for ip in ip_addresses:
        threads.append(
            ThreadWithResult(
                target=print_version_sem,
                args=(ip,),
            ),
        )

    for t in threads:
        t.start()

    results = []
    for t in threads:
        results.append(t.join())

    for r in results:
        print(r)
