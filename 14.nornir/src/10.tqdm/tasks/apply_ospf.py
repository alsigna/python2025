from nornir.core.task import Result, Task

from .configure_ospf import configure_ospf


def apply_ospf(task: Task) -> Result:
    result = task.run(task=configure_ospf, undo=False, severity_level=10)
    return result
