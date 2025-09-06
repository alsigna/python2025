from pathlib import Path

from nornir import InitNornir
from nornir.core.task import Result, Task
from nornir_rich.functions import print_result
from nornir_rich.progress_bar import RichProgressBar
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result as print_result_legacy
from nornir_utils.plugins.processors import PrintResult
from plugins.processors import LogProcessor
from tasks.demo import demo

if __name__ == "__main__":
    nr = InitNornir(config_file=Path(Path(__file__).parent, "config.yaml"))
    # nr_proc = nr.with_processors([PrintResult(), RichProgressBar()])
    # nr_proc = nr.with_processors([RichProgressBar()])
    result = nr.with_processors(
        [
            # from nornir_utils.plugins.processors import PrintResult
            # PrintResult(),
            # from plugins.processors import LogProcessor
            LogProcessor(),
            # from nornir_rich.progress_bar import RichProgressBar
            RichProgressBar(),
        ],
    ).run(task=demo)

    print("-" * 50)
    # print_result(result, severity_level=10)
