from textual.app import App

from textual.widgets import Header
from textual.widgets import Footer

from textual.widgets import Button

from textual.containers import Vertical


class CacheCleanerMenu(App):

    CSS = """

    Screen {

        align: center middle;

    }

    Vertical {

        width: 50;

        height: auto;

    }

    Button {

        margin: 1;

    }

    """

    def compose(self):

        yield Header()

        yield Vertical(

            Button(
                "Scan System",
                id="scan"
            ),

            Button(
                "Clean Cache",
                id="clean"
            ),

            Button(
                "View Report",
                id="report"
            ),

            Button(
                "Exit",
                id="exit"
            )

        )

        yield Footer()

    def on_button_pressed(
        self,
        event
    ):

        buttonId = event.button.id

        if buttonId == "scan":

            self.notify(
                "Scanning Started"
            )

        elif buttonId == "clean":

            self.notify(
                "Cleaning Started"
            )

        elif buttonId == "report":

            self.notify(
                "Opening Report"
            )

        elif buttonId == "exit":

            self.exit()


if __name__ == "__main__":

    app = CacheCleanerMenu()

    app.run()