from rich.live import Live
from rich.text import Text
from rich.console import Console
import time

console=Console()
def deletee():
    files=[

        "cache.db",
        "image.tmp",
        "chrome.log",
        "session.cache"
    ]
    with Live(refresh_per_second=4)as live:
        for file in files:
            live.update(
                Text(f"files Deleting :{file}",
                     style="red")

            )
            time.sleep(1)

def showDeleting(path):

    import os

    fileName = os.path.basename(path)

    console.print(
        f"[red]Deleting:[/red] {fileName}"
    )