from pathlib import Path

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_rich.functions import print_result
from nornir_rich.progress_bar import RichProgressBar
from nornir_scrapli.tasks import send_command
from plugins.processors import LogProcessor


def cisco_main(task: Task) -> Result:
    commands = ["show version", "show clock", "show inventory"]
    for command in commands:
        task.run(task=send_command, command=command, name=f"вывод '{command}'", severity_level=20)


def huawei_main(task: Task) -> Result:
    commands = ["display version", "display clockk", "display device"]
    for command in commands:
        task.run(task=send_command, command=command, name=f"вывод '{command}'", severity_level=20)


def demo(task: Task) -> Result:
    task.severity_level = 10
    if task.host.platform == "cisco_iosxe":
        task.run(cisco_main)
    elif task.host.platform == "huawei_vrp":
        task.run(huawei_main)
    return Result(
        host=task.host,
        result="сбор закончен",
    )
