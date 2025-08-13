from log import rich_log
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.plugins.runners import RunnersPluginRegister
from plugins.functions import print_table
from plugins.inventory import DynamicInventory
from plugins.processors import RichProcessor
from plugins.runners.fibonacci import FibonacciThreadedRunner
from tasks import demo

InventoryPluginRegister.register("DynamicInventory", DynamicInventory)
RunnersPluginRegister.register("FibonacciThreadedRunner", FibonacciThreadedRunner)

if __name__ == "__main__":
    nr = InitNornir(
        runner={
            "plugin": "FibonacciThreadedRunner",
            "options": {
                "num_workers": 8,
            },
        },
        inventory={"plugin": "DynamicInventory"},
        logging={"enabled": False},
    )
    result = nr.with_processors(
        [RichProcessor(rich_log)],
    ).run(task=demo)
    print_table(result)
