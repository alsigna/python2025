# inventory_plugins/dynamic_inventory.py

from nornir.core.inventory import ConnectionOptions, Defaults, Group, Host, Inventory, ParentGroups


class DynamicInventory:
    def __init__(self, **kwargs):
        self._inventory = self._build_inventory()

    def load(self) -> Inventory:
        return self._inventory

    def _build_inventory(self) -> Inventory:
        connection_options = {
            "scrapli": ConnectionOptions(
                extras={
                    "auth_strict_key": False,
                    "transport": "system",
                    "transport_options": {
                        "open_cmd": [
                            "-o KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                            "-o HostKeyAlgorithms=+ssh-rsa",
                        ],
                    },
                },
            ),
        }

        defaults = Defaults(
            username="admin",
            password="P@ssw0rd",  # noqa: S106
            port=22,
            connection_options=connection_options,
        )

        groups = {
            "cisco": Group(
                name="cisco",
                platform="cisco_iosxe",
            ),
            "huawei": Group(
                name="huawei",
                platform="huawei_vrp",
            ),
        }

        hosts = {
            f"r{i:02}": Host(
                name=f"r{i:02}",
                hostname=f"192.168.122.11{i%10}",
                groups=ParentGroups([groups["cisco"]]),
                defaults=defaults,
            )
            for i in range(10)
        }

        return Inventory(
            hosts=hosts,
            groups=groups,
            defaults=defaults,
        )
