type ScrapliDict = dict[str, str | bool | int | dict[str, list[str]]]


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


if __name__ == "__main__":
    collect_output(scrapli, "show version")
