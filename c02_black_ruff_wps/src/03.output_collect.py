# poetry run black --check 02.black_ruff_wps/src/03.output_collect.py
# poetry run ruff check 02.black_ruff_wps/src/03.output_collect.py
# poetry run flake8 02.black_ruff_wps/src/03.output_collect.py
from scrapli import Scrapli
from scrapli.response import MultiResponse

SCRAPLI_TEMPLATE = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}

DEVICES = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.103",
]


def send_commands(scrapli_params: dict[str, str], commands: list[str]) -> MultiResponse:
    with Scrapli(**scrapli_params) as ssh:
        return ssh.send_commands(
            commands=commands,
            stop_on_failed=True,
        )


if __name__ == "__main__":
    for device in DEVICES:
        try:
            result = send_commands(
                scrapli_params=SCRAPLI_TEMPLATE | {"host": device},
                commands=[
                    "show ip arp",
                    "show ip int br",
                    "show version",
                ],
            )
        except Exception as exc:
            print(f"{device}: исключение {exc.__class__.__name__} - {str(exc)}")
        else:
            print(f"{device}: вывод команд:")
            print(result.result)
        print("-" * 20)
