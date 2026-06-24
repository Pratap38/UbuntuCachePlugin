from textual.app import App

from textual.widgets import Header
from textual.widgets import Footer

from textual.widgets import Checkbox

from textual.widgets import Button

from textual.containers import Vertical


class CacheSelectionScreen(App):

    CSS = """

    Screen {

        align:center middle;

    }

    Vertical {

        width:60;
        height:auto;

    }

    Checkbox {

        margin:1;

    }

    Button {

        margin-top:2;

    }

    """

    def compose(self):

        yield Header()

        yield Vertical(

            Checkbox(
                "User Cache",
                value=True,
                id="user_cache"
            ),

            Checkbox(
                "APT Cache",
                value=False,
                id="apt_cache"
            ),

            Checkbox(
                "Temp Files",
                value=True,
                id="temp_files"
            ),

            Checkbox(
                "Thumbnail Cache",
                value=True,
                id="thumbnail"
            ),

            Checkbox(
                "Browser Cache",
                value=True,
                id="browser"
            ),

            Checkbox(
                "Trash",
                value=True,
                id="trash"
            ),

            Button(
                "Start Cleaning",
                id="start"
            )

        )

        yield Footer()

    def on_button_pressed(
        self,
        event
    ):

        if event.button.id == "start":

            selectedCaches = []

            if self.query_one(
                "#user_cache",
                Checkbox
            ).value:

                selectedCaches.append(
                    "User Cache"
                )

            if self.query_one(
                "#apt_cache",
                Checkbox
            ).value:

                selectedCaches.append(
                    "APT Cache"
                )

            if self.query_one(
                "#temp_files",
                Checkbox
            ).value:

                selectedCaches.append(
                    "Temp Files"
                )

            if self.query_one(
                "#thumbnail",
                Checkbox
            ).value:

                selectedCaches.append(
                    "Thumbnail Cache"
                )

            if self.query_one(
                "#browser",
                Checkbox
            ).value:

                selectedCaches.append(
                    "Browser Cache"
                )

            if self.query_one(
                "#trash",
                Checkbox
            ).value:

                selectedCaches.append(
                    "Trash"
                )

            self.notify(
                f"Selected: {len(selectedCaches)} Categories"
            )

            print("\nSelected Caches:\n")

            for item in selectedCaches:

                print(item)


if __name__ == "__main__":

    app = CacheSelectionScreen()

    app.run()