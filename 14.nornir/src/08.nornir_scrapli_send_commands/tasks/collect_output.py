from nornir.core.task import Result, Task
from nornir_scrapli.tasks import send_commands


def collect_output(task: Task) -> Result:
    # print(task.host.data)
    # print(task.host.data["commands"])
    # print(task.host["commands"])

    result = task.run(
        task=send_commands,
        commands=task.host["commands"],
        severity_level=10,
    )
    text_result = result.result
    # task.run(
    #     task=echo_data,
    #     scrapli_result=text_result,
    #     severity_level=10,
    # )
    # scrapli_response: MultiResponse = result.scrapli_response
    return Result(host=task.host, result=text_result)
