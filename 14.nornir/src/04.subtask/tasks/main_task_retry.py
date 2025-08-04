import logging

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
    result = {}
    for task_result in task.results:
        result |= task_result.result
    return Result(host=task.host, result=result)


def check_port_status_level2_all_in_one(task: Task, ports: list[int]) -> Result:
    posts_str = map(str, ports)
    task.run(
        task=tcp_ping,
        ports=ports,
        timeout=3,
        name=f"tcp ping -> tcp/{','.join(posts_str)}",
    )
    return Result(host=task.host, result=task.results[0].result)


def check_port_status_level1(task: Task, ports: list[int], raise_on_failed: bool = False) -> Result:
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
    result = {}
    for task_result in task.results:
        result |= task_result.result
    retry_result = {}
    for port, status in result.items():
        if status:
            continue
        task_result = task.run(
            task=tcp_ping,
            ports=[port - 1],
            timeout=3,
            name=f"tcp ping -> tcp/{port} (retry)",
        )
        port_status = task_result[0].result[port - 1]
        retry_result |= {port: port_status}
    result |= retry_result
    failed = not all(result.values())
    return Result(
        host=task.host,
        result=result,
        failed=failed if raise_on_failed else False,
    )


def main_task_retry(task: Task) -> Result:
    ports = [22, 23, 25]
    task.run(
        task=check_port_status_level1,
        name="проверка статуса портов - level1",
        ports=ports,
        raise_on_failed=False,
        severity_level=logging.DEBUG,
    )
    opened_ports = [str(port) for port, opened in task.results[0].result.items() if opened]
    closed_ports = [str(port) for port, opened in task.results[0].result.items() if not opened]
    result = "{}. Открытые порты: {}. Закрытые порты {}.".format(
        task.host.name,
        ",".join(opened_ports) if len(opened_ports) != 0 else "нет",
        ",".join(closed_ports) if len(closed_ports) != 0 else "нет",
    )
    return Result(
        host=task.host,
        result=result,
    )
