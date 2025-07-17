from typing import Any


class NetworkDevice:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_output(self, command: str) -> str:
        print(f"собираем вывод '{command}' с устройства '{self.ip}'")
        return f"вывод команды '{command}'"


class Netbox:
    DEVICES = {
        "rt1": "192.168.1.1",
        "rt2": "192.168.2.1",
    }

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token

    def get_device(self, hostname: str) -> str:
        print(f"получаем информацию об '{hostname}' из '{self.url}'")
        return self.DEVICES[hostname]


class Redis:
    def __init__(self, url: str):
        self.url = url

    def store(self, data: dict[str, Any]) -> None:
        print(f"сохраняем данные в redis '{self.url}'")


class ConfigCollector:
    NETBOX_URL = "netbox.my.lab"
    NETBOX_TOKEN = "12345"  # noqa: S105
    REDIS_URL = "redis.my.lab"

    def __init__(
        self,
        hostname: str,
        netbox_url: str = "",
        netbox_token: str = "",
        redis_url: str = "",
    ):
        self.netbox = Netbox(
            url=netbox_url or self.NETBOX_URL,
            token=netbox_token or self.NETBOX_TOKEN,
        )
        self.redis = Redis(
            url=redis_url or self.REDIS_URL,
        )
        self.hostname = hostname
        self.device = NetworkDevice(
            ip=self.netbox.get_device(hostname),
        )

    def backup_config(self) -> None:
        config = self.device.get_output("show running")
        self.redis.store({self.hostname: config})


if __name__ == "__main__":
    cc = ConfigCollector("rt1")
    cc.backup_config()
