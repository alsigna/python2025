from collections import deque
from copy import deepcopy
from pathlib import Path
from typing import Sequence

from nornir import InitNornir
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result, Task
from nornir_scrapli.result import ScrapliResult
from nornir_scrapli.tasks.core.send_command import send_command
from nornir_utils.plugins.functions import print_result


def get_command_output(task: Task, command: str) -> Result:
    task.name = f"вывод команды: '{command}'"
    try:
        subtask_result: ScrapliResult = task.run(
            task=send_command,
            command=command,
            severity_level=10,
        )
    except NornirSubTaskError as exc:
        subtask_exc = exc.result.exception
        status = f"Ошибка сбора команды '{command}'"
        if subtask_exc is None:
            result = exc.result.result.strip()
        else:
            result = f"{subtask_exc.__class__.__name__}: {subtask_exc}"
        failed = True
        print(
            "ошибка во время выполнения задачи '{}'. устройств '{}', команда '{}'. {}".format(
                task.name,
                task.host.name,
                command,
                result,
            ),
        )
    except Exception as exc:
        status = f"Ошибка сбора команды '{command}'"
        result = f"{exc.__class__.__name__}: {exc}"
        failed = True
        print(
            "неизвестная ошибка во время выполнения задачи '{}'. устройств '{}', команда '{}'. {}".format(
                task.name,
                task.host.name,
                command,
                f"{exc.__class__.__name__}: {exc}",
            ),
        )
    else:
        status = f"Команда '{command}' собрана успешно"
        result = subtask_result.result
        failed = False

    return Result(
        host=task.host,
        status=status,
        result=result,
        failed=failed,
    )


def main_cisco(task: Task) -> Result:
    for command in (
        "show version",
        "show clock",
        "show inventory",
    ):
        task.run(
            task=get_command_output,
            command=command,
            severity_level=20,
        )


def main_huawei(task: Task) -> Result:
    for command in (
        "display version",
        "display clock",
        "display device",
    ):
        task.run(
            task=get_command_output,
            command=command,
            severity_level=20,
        )


def main(task: Task) -> Result:
    if task.host.platform == "cisco_iosxe":
        task.run(task=main_cisco)
    elif task.host.platform == "huawei_vrp":
        task.run(task=main_huawei)


if __name__ == "__main__":
    nr = InitNornir(
        config_file=Path(Path(__file__).parent, "config.yaml"),
        # core={"raise_on_error": True},
    )
    result = nr.run(task=main, severity_level=10)

    # множество неуспешных устройств
    print(f"{nr.data.failed_hosts=}")
    for host in nr.data.failed_hosts:
        print(f"задачи для '{host}' завершились с ошибкой")

    # стек неуспешных задач
    # два примера
    # - с неправильной командой
    # - отключить ssh
    for host, tasks_result in result.failed_hosts.items():
        host_tasks = deque([(0, t) for t in tasks_result])
        while len(host_tasks) != 0:
            level, task = host_tasks.popleft()
            if isinstance(task, Sequence):
                host_tasks.extend([(level + 1, t) for t in task])
            elif task.failed:
                print(f"{' '*level}{host}: {task.name=}, {task.failed=}, {task.exception=}")

    # повторим для неудачных устройств
    if nr.data.failed_hosts:
        for host in nr.data.failed_hosts:
            # переключимся на telnet
            scrapli_ssh = nr.inventory.hosts[host].get_connection_parameters("scrapli")
            scrapli_telnet = deepcopy(scrapli_ssh)
            scrapli_telnet.port = 23
            scrapli_telnet.extras["transport"] = "telnet"
            nr.inventory.hosts[host].connection_options |= {"scrapli": scrapli_telnet}
        retry_result = nr.run(
            task=main,
            severity_level=10,
            on_good=False,
            on_failed=True,
        )
        for host in list(nr.data.failed_hosts):
            if host not in retry_result.failed_hosts:
                nr.data.recover_host(host)
                result[host] = retry_result[host]

    print_result(
        result,
        vars=["status"],
    )
