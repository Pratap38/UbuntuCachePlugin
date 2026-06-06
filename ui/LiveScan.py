from rich.console import Console
from rich.status import Status
from Scanner.scan_engine import scanAll
import time

console=Console()

def showScanner():
    with console.status(
        "[green]Scanning Cache ....[green]"
    ):
        time.sleep(3)
        result=scanAll()
    return result