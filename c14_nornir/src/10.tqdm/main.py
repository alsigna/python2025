from pathlib import Path

from nornir import InitNornir
from tasks import configure_ospf
from tqdm import tqdm

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(
        config_file=Path(cwd, "config.yaml"),
        # dry_run=True,
    )
    with tqdm(
        total=len(nr.inventory.hosts),
        desc="Настройка OSPF",
    ) as pb:
        result = nr.run(
            task=configure_ospf,
            progress_bar=pb,
            undo=False,
        )
    # print_result(result)
