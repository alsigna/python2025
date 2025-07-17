from typing import Any

from rich import box
from rich.console import Console
from rich.table import Table
from scrapli import Scrapli
from scrapli.response import MultiResponse

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": True,
}


def send_commands(device: dict[str, Any], commands: list[str]) -> MultiResponse:
    with Scrapli(**device) as ssh:
        return ssh.send_commands(
            commands=commands,
            stop_on_failed=True,
        )


def print_table(data: list[dict[str, Any]], title: str) -> None:
    table = Table(title=title, box=box.SQUARE_DOUBLE_HEAD)
    columns = data[0].keys()

    for col in columns:
        table.add_column(str(col), style="cyan")

    for row in data:
        row_values = [str(row.get(col, "")) for col in columns]
        table.add_row(*row_values)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    try:
        result = send_commands(
            device,
            [
                "show ip arp",
                "show ip interface brief",
            ],
        )
    except Exception as exc:
        print(f"ошибка {exc.__class__.__name__}: {str(exc)}")
    else:
        for r in result:
            print("-" * 100)
            print(f"command: {r.channel_input}")
            print(f"raw output:\n{r.result}\n")
            print_table(r.textfsm_parse_output(), r.channel_input)  # type: ignore [arg-type]
