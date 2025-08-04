from nornir.core.task import Result, Task

from .configure_ospf import configure_ospf


def destroy_ospf(task: Task) -> Result:
    result = task.run(task=configure_ospf, undo=True, severity_level=10)
    return result
