import re

from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result, Task
from nornir_scrapli.tasks import send_command
from scrapli.response import Response


def demo(task: Task) -> Result:
    if task.host.platform == "cisco_iosxe":
        command = "show version"
    elif task.host.platform == "huawei_vrp":
        command = "display versions"
    else:
        raise ValueError(f"неизвестная платформа {task.host.platform}")
    try:
        result = task.run(
            task=send_command,
            command=command,
            name=f"вывод '{command}'",
            severity_level=10,
        )
    except NornirSubTaskError:
        return Result(
            host=task.host,
            result="",
            uptime="",
            version="",
        )
    scrapli_response: Response = result.scrapli_response
    uptime = re.search(r"\suptime\sis\s(.*)", scrapli_response.result).group(1)
    uptime = uptime.lstrip("0wekday, ")
    version = re.search(r"\sVersion\s(\S+?),?\s", scrapli_response.result).group(1)
    return Result(
        host=task.host,
        result=scrapli_response.result,
        uptime=uptime,
        version=version,
    )
