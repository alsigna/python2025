from nornir.core.task import Result, Task
from nornir_scrapli.tasks.core.send_command import send_command


def save_config(task: Task) -> Result:
    commands = {
        "cisco_iosxe": "write memory",
        "huawei_vrp": "save",
    }
    result = task.run(
        task=send_command,
        command=commands.get(task.host.platform),
        severity_level=10,
    )
    return Result(
        host=task.host,
        result=result.result,
        scrapli_response=result.scrapli_response,
    )
