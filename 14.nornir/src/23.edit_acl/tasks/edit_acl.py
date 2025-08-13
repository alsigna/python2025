from nornir.core.task import Result, Task
from nornir_scrapli.result import ScrapliResult
from nornir_scrapli.tasks.core.send_command import send_command


def edit_acl(task: Task) -> Result:
    output: ScrapliResult = task.run(
        task=send_command,
        command="show ip access-lists ",
        severity_level=10,
    )
    return Result(
        host=task.host,
        result=output.scrapli_response.result,
    )
