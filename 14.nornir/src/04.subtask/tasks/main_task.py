from nornir.core.task import Result, Task


def sub_task4_level2(task: Task) -> Result:
    return Result(
        host=task.host,
        result="результат задачи 'sub_task4_level2'",
    )


def sub_task5_level2(task: Task) -> Result:
    return Result(
        host=task.host,
        result="результат задачи 'sub_task5_level2'",
    )


def sub_task1_level1(task: Task) -> Result:
    task.run(task=sub_task4_level2, name="подзадача-4, уровень-2")
    task.run(task=sub_task5_level2, name="подзадача-5, уровень-2")


def sub_task2_level1(task: Task) -> Result:
    return Result(
        host=task.host,
        result="результат задачи 'sub_task2_level1'",
    )


def sub_task3_level1(task: Task) -> Result:
    task.run(task=sub_task4_level2, name="подзадача-4, уровень-2")
    return Result(
        host=task.host,
        result="результат задачи 'sub_task3_level1'",
    )


def main_task(task: Task) -> Result:
    task.run(task=sub_task1_level1, name="подзадача-1, уровень-1")
    task.run(task=sub_task2_level1, name="подзадача-2, уровень-1")
    task.run(task=sub_task3_level1, name="подзадача-3, уровень-1")
    return Result(
        host=task.host,
        result="результат задачи 'main_task'",
    )
