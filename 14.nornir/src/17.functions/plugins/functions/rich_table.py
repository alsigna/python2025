from nornir.core.task import AggregatedResult
from rich import box
from rich.console import Console
from rich.table import Table


def print_table(results: AggregatedResult, vars: list[str] | None = None) -> None:
    console = Console()
    if vars is None:
        vars = ["result"]

    table = Table(show_lines=True, box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("host", justify="right", style="cyan", no_wrap=True)
    for col in vars:
        table.add_column(col)

    for host, result in results.items():
        row = [host]
        row.extend(getattr(result, field) for field in vars)
        table.add_row(*row)

    console.print(table)
