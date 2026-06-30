from textual.app import App
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Checkbox
from textual.widgets import Button
from textual.widgets import Select
from textual.containers import Vertical

from ui.CleanScreen import CleaningScreen
from core.CleaningPreset import CleaningPreset


class CacheSelectionScreen(App):

    CSS = """

    Screen {

        align: center middle;

    }

    Vertical {

        width: 60;
        height: auto;

    }

    Select {

        margin-bottom: 1;

    }

    Checkbox {

        margin: 1;

    }

    Button {

        margin-top: 2;

    }

    """

    def compose(self):

        yield Header()

        yield Vertical(

            Select(

                [

                    (preset, preset)

                    for preset in CleaningPreset.allPreset()

                ],

                prompt="Select Cleaning Preset",

                id="preset"

            ),

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

    def on_select_changed(self, event):

        if event.select.id != "preset":

            return

        preset = event.value

        selectedCaches = CleaningPreset.getPreset(

            preset

        )

        self.query_one(

            "#user_cache",

            Checkbox

        ).value = "User Cache" in selectedCaches

        self.query_one(

            "#apt_cache",

            Checkbox

        ).value = "APT Cache" in selectedCaches

        self.query_one(

            "#temp_files",

            Checkbox

        ).value = "Temp Files" in selectedCaches

        self.query_one(

            "#thumbnail",

            Checkbox

        ).value = "Thumbnail Cache" in selectedCaches

        self.query_one(

            "#browser",

            Checkbox

        ).value = "Browser Cache" in selectedCaches

        self.query_one(

            "#trash",

            Checkbox

        ).value = "Trash" in selectedCaches

    def on_button_pressed(self, event):

        if event.button.id != "start":

            return

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

        self.push_screen(

            CleaningScreen(

                selectedCaches

            )

        )


if __name__ == "__main__":

    app = CacheSelectionScreen()

    app.run()