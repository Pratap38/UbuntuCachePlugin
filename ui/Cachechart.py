from rich.console import Console
from rich.table import Table

from core.utils import format_size

def showCacheChart(results):
    console = Console()

    table = Table(
        title="Cache Breakdown"
    )

    table.add_column("Category")

    table.add_column("Usage")

    table.add_column("Size")
    maxSize = max(
        category.size
        for category in results
    )
    for category in results:

        ratio = category.size / maxSize

        barLength = int(ratio * 30)

        bar = "█" * barLength

        table.add_row(
            category.name,
            bar,
            format_size(category.size)
        )
    console.print(table)