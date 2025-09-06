from logging import Logger

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Task


# ⏩
# ✅
class LogProcessor:
    def __init__(self, log: Logger) -> None:
        self.log = log

    def task_started(self, task: Task) -> None:
        """This method is called right before starting the task."""
        self.log.warning(f"задача '{task.name}' запущена task_started")

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        """This method is called when all the hosts have completed executing their respective task."""

    def task_instance_started(self, task: Task, host: Host) -> None:
        """This method is called before a host starts executing its instance of the task."""
        self.log.info(f"LogProcessor: task_instance_started {task.name} / {host.name}")

    def task_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """.This method is called when a host completes its instance of a task."""

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        """This method is called before a host starts executing a subtask."""

    def subtask_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """This method is called when a host completes executing a subtask."""
