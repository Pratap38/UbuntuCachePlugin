from rich.progress import Progress
import time

def progress():
    with Progress() as progresses:
        task=progresses.add_task(
            "[blue]Scanning ...[blue]",
            total=100

        )
        for i in range(100):
            time.sleep(0.5)
            progresses.update(
                task,
                advance=1
            )
