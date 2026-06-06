from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from core.utils import format_size
console=Console()

def showHeader():
   pannel = Panel(
    "[bold yellow]Ubuntu Cache Cleaner[/bold yellow]\n"
    "[red]System Cleanup & Analysis Tool[red]",
    title="[blue]Version 1.0[blue]"
)
   console.print(pannel)

def showTable(results):
    table=Table(
        title  =" System Cache  Analysis"

    )
    table.add_column("Category")
    table.add_column("Files")
    table.add_column("Size")
    table.add_column("Risk")
    for category in results:
        table.add_row(
            category.name,
            str(category.files),
            format_size(category.size),
            category.riskLevel
        )
    console.print(table)

