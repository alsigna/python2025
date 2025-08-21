import difflib
import re
from pathlib import Path

from jinja2 import Environment
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks.template_file import template_file
from nornir_scrapli.result import ScrapliResult
from nornir_scrapli.tasks.core.send_command import send_command
from nornir_scrapli.tasks.core.send_configs import send_configs


def get_acl_diff_tuples(current_acl: str, target_acl: str) -> list[tuple[str, str]]:
    current_lines = current_acl.splitlines()
    target_lines = target_acl.splitlines()
    matcher = difflib.SequenceMatcher(None, current_lines, target_lines)

    result: list[tuple[str, str]] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "delete":
            for line in current_lines[i1:i2]:
                result.append((line, ""))
        elif tag == "insert":
            for line in target_lines[j1:j2]:
                result.append(("", line))
        elif tag == "replace":
            old_block = current_lines[i1:i2]
            new_block = target_lines[j1:j2]
            max_len = max(len(old_block), len(new_block))
            for k in range(max_len):
                old_ace = old_block[k] if k < len(old_block) else None
                new_ace = new_block[k] if k < len(new_block) else None
                if old_ace and new_ace:
                    result.append((old_ace, new_ace))
                elif old_ace:
                    result.append((old_ace, ""))
                elif new_ace:
                    result.append(("", new_ace))

    return result


def parse_acl(config: str) -> dict[str, str]:
    result = {}
    config = f"!\n{config}\n!"
    for acl in re.finditer(
        pattern=r"(?<=\n)ip access-list extended (?P<name>\S+)(?P<entries>.*?)\n(?=\S)",
        string=config,
        flags=re.DOTALL,
    ):
        result[acl.group("name")] = acl.group("entries").lstrip("\n")
    return result


def get_diff(task: Task, current_config: str, target_config: str) -> Result:
    current_acls = parse_acl(current_config)
    target_acls = parse_acl(target_config)

    diff = []
    for acl_name, acl_entries in target_acls.items():
        entrypoint = f"ip access-list extended {acl_name}"
        if acl_name not in current_acls:
            diff.append(entrypoint)
            diff.extend(acl_entries.splitlines())
            continue

        acl_diff = get_acl_diff_tuples(current_acls[acl_name], target_acls[acl_name])

        if not acl_diff:
            continue
        diff.append(entrypoint)
        for current_ace, target_ace in acl_diff:
            if not current_ace:
                diff.append(target_ace)
            else:
                seq = current_ace.split()[0].strip()
                diff.append(f" no {seq}")
                if target_ace:
                    diff.append(target_ace)

    return Result(
        host=task.host,
        result=diff,
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
