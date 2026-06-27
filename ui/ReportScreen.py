from textual.screen import Screen
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Static
from textual.widgets import Button
from textual.containers import Vertical


class ReportScreen(Screen):

    def __init__(self, results):

        super().__init__()

        self.results = results

    def compose(self):

        success = 0
        failed = 0
        report = ""

        for cache, status in self.results.items():

            if status:
                report += f"✓ {cache}\n"
                success += 1
            else:
                report += f"✗ {cache}\n"
                failed += 1

        report += "\n"
        report += f"Success : {success}\n"
        report += f"Failed  : {failed}\n"

        yield Header()

        yield Vertical(
            Static(report, id="report"),
            Button("Back To Menu", id="back")
        )

        yield Footer()

    def on_button_pressed(self, event):

        if event.button.id == "back":
            self.app.pop_screen()  # pop ReportScreen
            self.app.pop_screen()  # pop CleaningScreen → back to menu