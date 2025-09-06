from pathlib import Path

from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file


def generate_ospf_config(task: Task, undo: bool = False) -> Result:
    template = f"{'undo_' if undo else ''}ospf_{task.host.platform}.j2"
    result = task.run(
        task=template_file,
        template=template,
        path=Path(Path(__file__).parent.parent, "templates"),
    )
    task.name += f" ({task.host.platform})"
    return Result(host=task.host, result=result.result, changed=False)
