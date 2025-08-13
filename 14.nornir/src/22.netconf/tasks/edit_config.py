import difflib
from pathlib import Path

from lxml import etree
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_netconf.plugins.tasks import netconf_commit, netconf_edit_config, netconf_get_config, netconf_rpc


def get_diff(running: Result, candidate: Result) -> str:
    running_xml = running.result.rpc.data_xml
    running_tree = etree.fromstring(running_xml.encode())  # noqa: S320
    running_str = etree.tostring(running_tree, pretty_print=True, encoding="unicode")

    candidate_xml = candidate.result.rpc.data_xml
    candidate_tree = etree.fromstring(candidate_xml.encode())  # noqa: S320
    candidate_str = etree.tostring(candidate_tree, pretty_print=True, encoding="unicode")

    diff = "\n".join(
        difflib.unified_diff(
            running_str.splitlines(),
            candidate_str.splitlines(),
            fromfile="running",
            tofile="candidate",
            lineterm="",
        ),
    )
    return diff


def get_acl_config(task: Task, target: str = "running") -> Result:
    task.name += f" ({target})"
    result = task.run(
        task=template_file,
        template="filter_acl.j2",
        path=Path(Path(__file__).parent.parent, "templates"),
    )
    result = task.run(
        task=netconf_get_config,
        source=target,
        path=result.result,
        filter_type="subtree",
    )
    return Result(
        host=task.host,
        result=result.result,
    )


def edit_acl(task: Task) -> Result:
    running = task.run(
        task=get_acl_config,
        target="running",
        severity_level=10,
    )
    config = task.run(
        task=template_file,
        template="config_acl.j2",
        path=Path(Path(__file__).parent.parent, "templates"),
        severity_level=10,
    )
    task.run(
        task=netconf_edit_config,
        config=config.result,
        target="candidate",
        severity_level=10,
        # default_operation="replace",
    )
    candidate = task.run(
        task=get_acl_config,
        target="candidate",
        severity_level=10,
    )
    diff = get_diff(running, candidate)
    if task.is_dry_run():
        task.name += " (dry-run)"
        task.run(
            task=netconf_rpc,
            payload="<discard-changes />",
            severity_level=10,
        )
    else:
        task.run(
            task=netconf_commit,
            severity_level=10,
        )

    return Result(
        host=task.host,
        result=diff or "Нет изменений",
    )
