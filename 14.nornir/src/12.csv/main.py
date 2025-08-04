from pathlib import Path

from nornir import InitNornir
from nornir.core.inventory import ConnectionOptions
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.task import Result, Task
from nornir_csv.plugins.inventory import CsvInventory
from nornir_scrapli.tasks.core.send_command import send_command
from nornir_utils.plugins.functions import print_result

InventoryPluginRegister.register("CsvInventoryPlugin", CsvInventory)


# CSVInventory - `poetry add nornir-table-inventory`
# CsvInventoryPlugin - `poetry add nornir-csv`


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
    nr.inventory.defaults.connection_options |= {
        "scrapli": ConnectionOptions(
            extras={
                "auth_strict_key": False,
                "transport": "system",
                "transport_options": {
                    "open_cmd": [
                        "-o KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                        "-o HostKeyAlgorithms=+ssh-rsa",
                    ],
                },
            },
        ),
    }
    nr.inventory.defaults.port = int(nr.inventory.defaults.port)
    result = nr.run(task=main)
    print_result(result)
