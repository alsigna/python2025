from random import getrandbits

from nornir.core.task import Result, Task


def my_random_task(task: Task, some_text: str) -> Result:
    print(f"raw print из тела задачи для устройства '{task.host}'")
    return Result(
        host=task.host,
        result=f"{task.host.name} выполнена с аргументом {some_text=}",
        changed=bool(getrandbits(1)),
    )
