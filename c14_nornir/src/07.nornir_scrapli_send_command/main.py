from pathlib import Path

from nornir import InitNornir
from nornir_scrapli.functions import print_structured_result
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from scrapli.logging import enable_basic_logging

enable_basic_logging("./debug.log", "DEBUG")

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        name="get version",
        task=send_command,
        command="show version",
    )
    print_structured_result(result)
    print_result(result)
