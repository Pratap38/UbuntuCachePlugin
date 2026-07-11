from textual.app import App
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Checkbox
from textual.widgets import Button
from textual.widgets import Select
from textual.containers import Vertical

from ui.CleanScreen import CleaningScreen
from core.CleaningPreset import CleaningPreset
from core.ConfigManager import ConfigManager


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

    def __init__(self):

        super().__init__()

        self.config = ConfigManager()

    def compose(self):

        yield Header()

        yield Vertical(

            Select(

                [

                    (preset, preset)

                    for preset in CleaningPreset.allPreset()

                ],

                value=self.config.get(
                    "defaultPreset"
                ),

                id="preset"

            ),

            Checkbox(
                "User Cache",
                id="user_cache"
            ),

            Checkbox(
                "APT Cache",
                id="apt_cache"
            ),

            Checkbox(
                "Temp Files",
                id="temp_files"
            ),

            Checkbox(
                "Thumbnail Cache",
                id="thumbnail"
            ),

            Checkbox(
                "Browser Cache",
                id="browser"
            ),

            Checkbox(
                "Trash",
                id="trash"
            ),

            Button(
                "Start Cleaning",
                id="start"
            )

        )

        yield Footer()

    def on_mount(self):

        preset = self.config.get(

            "defaultPreset"

        )

        self.applyPreset(

            preset

        )

    def applyPreset(

        self,

        preset

    ):

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

    def on_select_changed(self, event):

        if event.select.id != "preset":

            return

        self.applyPreset(

            event.value

        )

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