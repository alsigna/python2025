from pathlib import Path

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import configure_ospf

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(
        config_file=Path(cwd, "config.yaml"),
        # dry_run=True,
    )
    result = nr.run(
        task=configure_ospf,
        undo=False,
    )
    print_result(result)
