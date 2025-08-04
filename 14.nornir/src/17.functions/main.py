from pathlib import Path

from nornir import InitNornir
from nornir_rich.functions import print_failed_hosts, print_inventory, print_result
from plugins.functions.print_summary import print_summary
from plugins.functions.rich_table import print_table
from tasks.demo import demo

if __name__ == "__main__":
    nr = InitNornir(config_file=Path(Path(__file__).parent, "config.yaml"))
    result = nr.run(task=demo)
    print_result(result, vars=["uptime", "version"])
    print_table(result, vars=["uptime", "version"])
    print_failed_hosts(result)
    print_inventory(nr.inventory)
    print_summary(result)
