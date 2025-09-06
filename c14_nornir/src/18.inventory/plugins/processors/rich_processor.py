from logging import Logger

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Task
from rich.console import Console


class RichProcessor:
    def __init__(self, log: Logger) -> None:
        self.console = Console()
        self.log = log

    def task_started(self, task: Task) -> None:
        self.console.rule(f"[bold green] Старт: [cyan]{task.name}")
        self.log.warning(f"старт задачи: [cyan]{task.name}")

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        self.console.rule(f"[bold green] Завершено: [cyan]{task.name}")

    def task_instance_started(self, task: Task, host: Host) -> None:
        self.log.info(f"выполнение [cyan]{task.name}[/cyan] на [green]{task.host}")

    def task_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        if result.failed:
            self.log.error(f"❌ [red]ошибка[/red] выполнения задачи [cyan]{task.name}[/cyan] на [green]{task.host}")
        else:
            self.log.debug(f"✅ задача [cyan]{task.name}[/cyan] на [green]{task.host}[/green] выполнена успешно")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        self.log.info(f"выполнение под-задачи [yellow]{task.name}[/yellow] на [green]{task.host}")

    def subtask_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        if result.failed:
            self.log.error(
                f"❌ [red]ошибка[/red] выполнения под-задачи [yellow]{task.name}[/yellow] на [green]{task.host}",
            )
        else:
            self.log.debug(
                f"✅ под-задача [yellow]{task.name}[/yellow] на [green]{task.host}[/green] выполнена успешно",
            )
