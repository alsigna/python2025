from pathlib import Path

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

# nr.filter(name="r10") - только определенное устройство (name это свойство устройства)
# nr.filter(platform="cisco_iosxe") - все устройства платформы (как и platform)
# nr.filter(role="access") - только с определенной роль, которая в data определена
# nr.filter(role="access", model="iosv") - роль access И модель iosv
# nr.filter(role="access").filter(model="iosv") - тот же результат, только цепочкой
# nr.filter(
#     F(role="access")
#     & F(model="iosv"),
# ) - тот же результат, только через F.
# nr.filter(
#     F(role="access")
#     | F(model="csr1000v"),
# ) - роль access ИЛИ модель csr1000v
# nr.filter(F(address__city="moscow")) - `__` для доступа к вложенным объектам
# nr.filter(F(groups__contains="msk")) - для проверки, что список содержит указанный элемент
# nr.filter(F(name__in=["r10", "r11"])) - для проверки, что значение входит в указанный список
# nr.filter(F(device_count__ge=50)) для фильтрации ge/le
# nr.filter(F(groups__all=["msk", "cisco"])) - all как аналог python функции all
# nr.filter(F(groups__any=["msk", "spb", "cisco"])) - аналог на any

if __name__ == "__main__":
    nr = InitNornir(
        runner={
            "plugin": "FibonacciThreadedRunner",
            "options": {"num_workers": 5},
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": Path(Path(__file__).parent, "inventory", "hosts.yaml"),
                "group_file": Path(Path(__file__).parent, "inventory", "groups.yaml"),
                "defaults_file": Path(Path(__file__).parent, "inventory", "defaults.yaml"),
            },
            "transform_function": "update_credentials",
        },
        logging={
            "enabled": False,
        },
    )
    result = nr.with_processors([RichProcessor(rich_log)]).run(task=demo)
    print_table(result)
