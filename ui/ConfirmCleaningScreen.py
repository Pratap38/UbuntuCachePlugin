
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Static, Button


class ConfirmCleaningScreen(ModalScreen[bool]):

    CSS = """
    ConfirmCleaningScreen {
        align: center middle;
    }

    #confirm_dialog {
        width: 60;
        height: auto;
        padding: 2;
        border: thick $primary;
        background: $surface;
    }

    #confirm_buttons {
        height: auto;
        align: center middle;
    }

    #confirm_buttons Button {
        margin: 1;
    }
    """

    def __init__(self, selectedCaches):
        super().__init__()
        self.selectedCaches = selectedCaches

    def compose(self):
        yield Vertical(
            Static(
                "Are you sure you want to clean these categories?",
                id="confirm_title",
            ),
            Static(
                "\n".join(f"• {cache}" for cache in self.selectedCaches),
                id="selected_caches",
            ),
            Static(
                "This operation may delete cache files.",
                id="confirm_warning",
            ),
            Vertical(
                Button("Confirm", variant="error", id="confirm"),
                Button("Cancel", variant="primary", id="cancel"),
                id="confirm_buttons",
            ),
            id="confirm_dialog",
        )

    def on_button_pressed(self, event):
        if event.button.id == "confirm":
            self.dismiss(True)
        elif event.button.id == "cancel":
            self.dismiss(False)
