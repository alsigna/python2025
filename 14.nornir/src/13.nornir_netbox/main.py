from pathlib import Path

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result


def main(task: Task) -> Result:
    command_map = {
        "cisco_iosxe": "show inventory",
        "huawei_vrp": "display device",
    }
    task.run(
        task=send_command,
        command=command_map[task.host.platform],
    )


if __name__ == "__main__":
    nr = InitNornir(config_file=Path(Path(__file__).parent, "config.yaml"))
    result = nr.run(task=main)
    print_result(result)
