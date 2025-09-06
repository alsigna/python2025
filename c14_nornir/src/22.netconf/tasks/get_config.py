from textwrap import dedent
from xml.dom.minidom import parseString

from nornir.core.task import Result, Task
from nornir_netconf.plugins.tasks import netconf_get_config


def get_config(task: Task) -> Result:
    filter_ = dedent(
        """
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname />
        </native>
        """,
    )
    result = task.run(
        task=netconf_get_config,
        path=filter_,
        filter_type="subtree",
        severity_level=10,
    )

    pretty_xml = parseString(  # noqa: S318
        result.result.rpc.xml,
    ).toprettyxml(
        indent="  ",
    )

    return Result(
        host=task.host,
        result=pretty_xml,
    )
