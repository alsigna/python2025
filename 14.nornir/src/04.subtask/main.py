from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import main_task

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        task=main_task,
        name="основная задача",
    )
    print_result(result)
