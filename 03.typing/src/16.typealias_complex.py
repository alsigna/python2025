from typing import Any, TypeAlias

# ScrapliDict: TypeAlias = dict[str, str | bool | int | dict[str, list[str]]]
ScrapliDict: TypeAlias = dict[str, Any]

scrapli: ScrapliDict = {
    "host": "192.168.0.1",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "transport": "system",
    "auth_strict_key": False,
    "port": 22,
    "transport_options": {
        "open_cmd": [
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ],
    },
    "timeout_ops": 120,
}


def collect_output(scrapli: ScrapliDict, command: str) -> str:
    return ""


def save_config(scrapli: ScrapliDict) -> None: ...


def reload(scrapli: ScrapliDict) -> None: ...


if __name__ == "__main__":
    collect_output(scrapli, "show version")
    reload()
