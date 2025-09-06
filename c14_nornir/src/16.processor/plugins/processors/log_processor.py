from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, MultiResult, Task


class LogProcessor:
    def task_started(self, task: Task) -> None:
        """This method is called right before starting the task."""
        print(f"LogProcessor: task_started {task.name}")

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        """This method is called when all the hosts have completed executing their respective task."""
        print(f"LogProcessor: task_completed {task.name}")

    def task_instance_started(self, task: Task, host: Host) -> None:
        """This method is called before a host starts executing its instance of the task."""
        print(f"LogProcessor: task_instance_started {task.name} / {host.name}")

    def task_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """.This method is called when a host completes its instance of a task."""
        print(f"LogProcessor: task_instance_completed {task.name} / {host.name} / {result.result}")

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        """This method is called before a host starts executing a subtask."""
        print(f"LogProcessor: subtask_instance_started {task.name} / {host.name}")

    def subtask_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """This method is called when a host completes executing a subtask."""
        print(f"LogProcessor: subtask_instance_completed {task.name} / {host.name} / {result.result}")
