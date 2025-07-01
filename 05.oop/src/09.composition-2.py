from types import TracebackType
from typing import Literal, Protocol, Self, runtime_checkable


class Scrapli:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def send_command(self, command: str) -> str:
        print(f"выполнение команды '{command}' с '{self.ip}'")
        return f"вывод '{command}' с '{self.ip}'"

    def open(self) -> None:
        print(f"сессия с '{self.ip}' открыта")

    def close(self) -> None:
        print(f"сессия с '{self.ip}' закрыта")

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self.close()
        return False


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.cli = Scrapli(ip)

    def __enter__(self) -> Self:
        self.cli.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self.cli.close()
        return False


@runtime_checkable
class CommandHandler(Protocol):
    def __init__(self, device: Device) -> None: ...
    def run(self) -> str: ...


class HandlerRegistry:
    _handlers: dict[str, type[CommandHandler]] = {}

    @classmethod
    def register(cls, handler: type[CommandHandler]) -> None:
        if not isinstance(handler, CommandHandler):
            raise TypeError(f"{handler.__name__} не реализует протокол CommandHandler")
        cls._handlers[handler.__name__] = handler

    @classmethod
    def get(cls, name: str) -> type[CommandHandler]:
        return cls._handlers[name]

    @classmethod
    def all(cls) -> list[CommandHandler]:
        return list(cls._handlers.values())


def register_handler(cls):
    HandlerRegistry.register(cls)
    return cls


@register_handler
class RunningCollector:
    def __init__(self, device: Device) -> None:
        self._device = device

    def run(self) -> str:
        running_config = self.get_running()
        running_config = self.prepare_running_config(running_config)
        return running_config

    def get_running(self) -> str:
        return self._device.cli.send_command("show version")

    def prepare_running_config(self, config: str) -> str:
        return config[::-1]


@register_handler
class RunningSaver:
    def __init__(self, device: Device) -> None:
        self._device = device

    def run(self) -> str:
        write_result = self.write_memory()
        return write_result

    def write_memory(self) -> str:
        return self._device.cli.send_command("write memory")


if __name__ == "__main__":
    with Device("1.2.3.4") as device:
        results: list[str] = []
        for handler in HandlerRegistry.all():
            print(f"{handler.__name__=}")
            print(f"{isinstance(handler, CommandHandler)=}")
            results.append(handler(device).run())
            print("-" * 10)

    print("\nрезультаты:")
    for result in results:
        print(result)
