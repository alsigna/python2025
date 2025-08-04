from random import getrandbits

from nornir.core.task import Result, Task
from nornir_utils.plugins.tasks.networking import tcp_ping


def check_port_status_level2_per_port(task: Task, ports: list[int]) -> Result:
    for port in ports:
        task.run(
            task=tcp_ping,
            ports=[port],
            timeout=3,
            name=f"tcp ping -> tcp/{port}",
        )


def check_port_status_level2_all_in_one(task: Task, ports: list[int]) -> Result:
    posts_str = map(str, ports)
    results = task.run(
        task=tcp_ping,
        ports=ports,
        timeout=3,
        name=f"tcp ping -> tcp/{','.join(posts_str)}",
    )
    failed = not all(result for result in results[0].result.values())
    return Result(host=task.host, failed=failed)


def check_port_status_level1(task: Task, ports: list[int]) -> Result:
    task.run(
        task=check_port_status_level2_per_port,
        name="проверка статуса портов - level2 (по отдельности)",
        ports=ports,
    )
    task.run(
        task=check_port_status_level2_all_in_one,
        name="проверка статуса портов - level2 (все разом)",
        ports=ports,
    )


def main_task_failed(task: Task) -> Result:
    ports = [22, 23, 24]
    task.run(
        task=check_port_status_level1,
        name="проверка статуса портов - level1",
        ports=ports,
    )
    return Result(
        host=task.host,
        result=f"{task.host.name} выполнена",
        changed=bool(getrandbits(1)),
    )
