from rich.console import Console

from rich.table import Table


console = Console()


def showRiskTable(results):

    table = Table(
        title="Cache Risk Analysis"
    )

    table.add_column(
        "Category",
        style="cyan"
    )

    table.add_column(
        "Risk Level"
    )

    table.add_column(
        "Recommendation"
    )

    for category in results:

        if category.riskLevel == "Safe":

            risk = "[green]SAFE[/green]"

            recommendation = (
                "[green]Can Clean Anytime[/green]"
            )

        elif category.riskLevel == "Medium":

            risk = "[yellow]WARNING[/yellow]"

            recommendation = (
                "[yellow]Review Before Cleaning[/yellow]"
            )

        else:

            risk = "[red]DANGEROUS[/red]"

            recommendation = (
                "[red]Advanced Users Only[/red]"
            )

        table.add_row(

            category.name,

            risk,

            recommendation

        )

    console.print(table)