from pathlib import Path

from nornir import InitNornir

if __name__ == "__main__":
    cwd = Path(__file__).parent
    nr = InitNornir(config_file=Path(cwd, "config.yaml"))
    # nr = InitNornir(
    #     inventory={
    #         "plugin": "SimpleInventory",
    #         "options": {
    #             "host_file": Path(cwd, "inventory", "hosts.yaml"),
    #             "group_file": Path(cwd, "inventory", "groups.yaml"),
    #             "defaults_file": Path(cwd, "inventory", "defaults.yaml"),
    #         },
    #     },
    #     logging={
    #         "enabled": True,
    #     },
    #     runner={
    #         "plugin": "threaded",
    #         "options": {
    #             "num_workers": 30,
    #         },
    #     },
    # )
