import asyncio

from textual.screen import Screen
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Static
from textual.widgets import ProgressBar
from textual import work

from cleaner.CleanerEngine import cleanSelectedCache
from ui.ReportScreen import ReportScreen


class CleaningScreen(Screen):

    def __init__(self, selectedCaches):

        super().__init__()

        self.selectedCaches = selectedCaches

        self.total = len(selectedCaches)

        self.completed = 0

        self.results = {}

    def compose(self):

        yield Header()

        yield Static(
            "Cleaning Selected Caches...",
            id="title"
        )

        yield Static(
            "Preparing...",
            id="status"
        )

        yield ProgressBar(
            total=self.total,
            id="progress"
        )

        yield Footer()

    def on_mount(self):

        self.startCleaning()

    @work(exclusive=True, thread=False)
    async def startCleaning(self):

        status = self.query_one(
            "#status",
            Static
        )

        progress = self.query_one(
            "#progress",
            ProgressBar
        )

        await asyncio.sleep(0.1)

        for cache in self.selectedCaches:

            status.update(
                f"Cleaning : {cache}"
            )

            cleanerResult = cleanSelectedCache(
                [cache]
            )

            self.results.update(
                cleanerResult
            )

            progress.advance(1)

            self.completed += 1

            await asyncio.sleep(0)

        status.update(
            "Cleaning Completed Successfully."
        )

        await asyncio.sleep(0.5)

        self.app.push_screen(

            ReportScreen(

                self.results

            )

        )