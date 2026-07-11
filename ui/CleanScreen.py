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

    @work(

        exclusive=True,

        thread=False

    )

    async def startCleaning(self):

        status = self.query_one(

            "#status",

            Static

        )

        progress = self.query_one(

            "#progress",

            ProgressBar

        )

        await asyncio.sleep(0.2)

        for cache in self.selectedCaches:

            status.update(

                f"Cleaning ({self.completed + 1}/{self.total}) : {cache}"

            )

            try:

                cleanerResult = cleanSelectedCache(

                    [cache]

                )

                self.results.update(

                    cleanerResult

                )

            except Exception:

                self.results[cache] = False

            progress.advance(

                1

            )

            self.completed += 1

            await asyncio.sleep(

                0.15

            )

        success = sum(

            self.results.values()

        )

        failed = self.total - success

        status.update(

            f"Completed | Success : {success}  Failed : {failed}"

        )

        await asyncio.sleep(

            0.8

        )

        self.app.push_screen(

            ReportScreen(

                self.results

            )

        )