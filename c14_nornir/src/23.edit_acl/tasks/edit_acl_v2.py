from pathlib import Path
from textwrap import dedent

from ctreepo import CTreeDiffer, CTreeEnv, Vendor
from jinja2 import Environment
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks.template_file import template_file
from nornir_scrapli.result import ScrapliResult
from nornir_scrapli.tasks.core.send_command import send_command
from nornir_scrapli.tasks.core.send_configs import send_configs


def get_diff(task: Task, current_config: str, target_config: str) -> Result:
    tagging_rules = [
        {"regex": r"^ip access-list extended (\S+)$", "tags": ["acl"]},
    ]
    mask = dedent(
        r"""
        ip access-list extended \S+
         (\d+) (:?permit|deny) .*         UNDO>> no \1
        """,
    )
    env = CTreeEnv(vendor=Vendor.CISCO, tagging_rules=tagging_rules)
    template = env.parse(mask)
    current = env.parse(current_config, template)
    current_acl = env.search(current, include_tags=["acl"])

    target = env.parse(target_config, template)
    target_acl = env.search(target, include_tags=["acl"])

    return Result(
        host=task.host,
        result=CTreeDiffer.diff(current_acl, target_acl).patch.splitlines(),
    )


def edit_acl(task: Task) -> Result:
    target_config = task.run(
        task=template_file,
        template="acl.j2",
        jinja_env=Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True),
        path=Path(Path(__file__).parent.parent, "templates"),
        severity_level=10,
    )
    current_config: ScrapliResult = task.run(
        task=send_command,
        command="show running-config",
        severity_level=10,
    )
    diff = task.run(
        task=get_diff,
        current_config=current_config.scrapli_response.result,
        target_config=target_config.result,
        severity_level=10,
    )
    if not diff.result:
        return Result(
            host=task.host,
            result="нет diff",
        )
    if task.is_dry_run():
        task.name += " (dry-run)"
        return Result(
            host=task.host,
            result="\n".join(diff.result),
        )

    result = task.run(
        task=send_configs,
        configs=diff.result,
        stop_on_failed=True,
        severity_level=10,
    )
    return Result(
        host=task.host,
        result=result.result,
    )
