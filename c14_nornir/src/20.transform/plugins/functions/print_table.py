from nornir.core.task import AggregatedResult
from rich import box
from rich.console import Console
from rich.table import Table

# box.


def print_table(results: AggregatedResult, variables: list[str] | None = None) -> None:
    console = Console()
    if variables is None:
        variables = ["result"]

    table = Table(show_lines=True, box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("host", justify="right", style="cyan", no_wrap=True)
    for col in variables:
        table.add_column(col)

    for host, result in results.items():
        if result.failed:
            row = [f"[bold red]{host}[/bold red]"]
        else:
            row = [host]
        row.extend(getattr(result, field).strip() for field in variables)
        table.add_row(*row)

    console.print(table)
