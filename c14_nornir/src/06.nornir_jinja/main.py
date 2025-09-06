import logging
from pathlib import Path

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result

# if __name__ == "__main__":
#     cwd = Path(__file__).parent
#     nr = InitNornir(config_file=Path(cwd, "config.yaml"))
#     result = nr.run(
#         name="генерация конфигурации ospf",
#         task=template_file,
#         template="ospf.j2",
#         path=Path(cwd, "templates"),
#     )
#     print_result(result)


# разные платформы (как пример)


def generate_ospf_config(task: Task) -> Result:
    template_name = f"ospf_{task.host.platform}.j2"
    result = task.run(
        task=template_file,
        template=template_name,
        path=Path(Path(__file__).parent, "templates"),
        severity_level=logging.DEBUG,
    )
    task.name += f" ({task.host.platform})"
    return Result(host=task.host, result=result.result, changed=False)


if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        name="генерация конфигурации ospf",
        task=generate_ospf_config,
    )
    print_result(result)
