from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import my_random_task

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        task=my_random_task,
        some_text="42",
        name="my test task",
    )
    print_result(result)
