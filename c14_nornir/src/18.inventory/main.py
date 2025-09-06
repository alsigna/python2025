from log import rich_log, simple_log
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from plugins.functions import print_table
from plugins.inventory import DynamicInventory
from plugins.processors import LogProcessor, RichProcessor
from tasks import demo

InventoryPluginRegister.register("DynamicInventory", DynamicInventory)


if __name__ == "__main__":
    nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 4}},
        inventory={"plugin": "DynamicInventory"},
        logging={"enabled": False},
    )
    result = nr.with_processors(
        [
            # LogProcessor(simple_log),
            RichProcessor(rich_log),
        ],
    ).run(task=demo)
    print_table(result)
