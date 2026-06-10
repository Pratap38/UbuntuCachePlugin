from rich.console import Console
from rich.panel import Panel

import core.report as reportData

from core.utils import format_size

console = Console()


def showFinalreport():

    spaceFreed = (
        reportData.beforeScanSize
        -
        reportData.afterScanSize
    )

    timeTaken = (
        reportData.endTime
        -
        reportData.startTime
    )

    reportText = f"""

Before Cleaning:
{format_size(reportData.beforeScanSize)}

After Cleaning:
{format_size(reportData.afterScanSize)}

Space Freed:
{format_size(spaceFreed)}

Time Taken:
{timeTaken:.2f} Seconds

Status:
SUCCESS

"""

    console.print(

        Panel(
            reportText,
            title="Final Cleaning Report"
        )

    )