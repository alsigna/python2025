import time
from random import randint

from nornir.core.task import Result, Task
from nornir_scrapli.tasks.core.send_command import send_command


def sub_sub_task(task: Task) -> Result:
    time.sleep(randint(50, 200) / 100)
    pass


def sub_task(task: Task) -> Result:
    time.sleep(randint(50, 200) / 100)
    task.run(task=sub_sub_task, name="sub-sub-task-1")
    task.run(task=sub_sub_task, name="sub-sub-task-2")


def demo(task: Task) -> Result:
    time.sleep(randint(50, 200) / 100)
    task.run(task=sub_task, name="sub-task-1")
    task.run(task=sub_task, name="sub-task-2")
    output = task.run(task=send_command, command="show clock", severity_level=10)
    return Result(
        host=task.host,
        changed=False,
        result=output.result,
    )
