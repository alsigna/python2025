from log import rich_log
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister, TransformFunctionRegister
from nornir.core.plugins.runners import RunnersPluginRegister
from plugins.functions import print_table
from plugins.inventory import DynamicInventory, update_credentials
from plugins.processors import RichProcessor
from plugins.runners.fibonacci import FibonacciThreadedRunner
from tasks import demo

InventoryPluginRegister.register("DynamicInventory", DynamicInventory)
TransformFunctionRegister.register("update_credentials", update_credentials)
RunnersPluginRegister.register("FibonacciThreadedRunner", FibonacciThreadedRunner)

if __name__ == "__main__":
    nr = InitNornir(
        runner={
            "plugin": "FibonacciThreadedRunner",
            "options": {"num_workers": 8},
        },
        inventory={
            "plugin": "DynamicInventory",
            "transform_function": "update_credentials",
        },
        logging={"enabled": False},
    )
    result = nr.with_processors([RichProcessor(rich_log)]).run(task=demo)
    print_table(result)
