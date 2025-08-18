from pathlib import Path

from nornir import InitNornir
from nornir_rich.functions import print_result

# from tasks.edit_acl_v1 import edit_acl
from tasks.edit_acl_v2 import edit_acl

if __name__ == "__main__":
    nr = InitNornir(
        config_file=Path(Path(__file__).parent, "config.yaml"),
        # dry_run=True,
    )
    result = nr.run(task=edit_acl)

    print_result(result)
