import logging
from pathlib import Path

from jinja2 import Template
from nornir.core.task import Result, Task

log = logging.getLogger("nornir.custom_jinja")


def custom_jinja(task: Task, template: Path) -> Result:
    with open(template, "r") as f:
        template_text = f.read()

    j2 = Template(
        template_text,
        lstrip_blocks=True,
        trim_blocks=True,
    )
    result = j2.render(host=task.host, data=task.host.data)
    log.debug(f"конфигурация для '{task.host.name}' сгенерирована")

    return Result(host=task.host, result=result)
