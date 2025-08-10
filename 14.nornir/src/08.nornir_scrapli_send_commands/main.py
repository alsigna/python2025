import logging
from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import backup_configuration, collect_output

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    result = nr.run(
        name="сбор выводов команд",
        task=collect_output,
    )
    # print_structured_result(result)
    print_result(result)

    # backup
    backup_folder = Path(cwd, "backup")
    result = nr.run(
        name="создание backup",
        task=backup_configuration,
        backup_folder=backup_folder,
    )
    print_result(result, severity_level=logging.DEBUG)
