import threading
import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from Scanner.parallelScan import ParallelScan

scanResult = None
scanComplete = False


def scanWorker():
    global scanResult
    global scanComplete

    scanResult = ParallelScan()
    scanComplete = True


def runAsyncscan():
    global scanComplete

    thread = threading.Thread(
        target=scanWorker
    )

    thread.start()

    console = Console()

    # Spinner frames
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    index = 0
    dots = 0

    with Live(
        refresh_per_second=12,
        console=console
    ) as live:

        while not scanComplete:

            # Spinner animation
            spin = spinner[index]
            index = (index + 1) % len(spinner)

            # Dot animation
            dots += 1
            if dots > 3:
                dots = 1

            message = (
                f"{spin} Scanning Cache"
                + "." * dots
            )

            live.update(
                Panel(
                    message,
                    title="Please Wait",
                    border_style="cyan"
                )
            )

            time.sleep(0.2)

    thread.join()

    return scanResult