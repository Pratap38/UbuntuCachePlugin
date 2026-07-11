from textual.screen import Screen
from textual.widgets import Header
from textual.widgets import Footer
from textual.widgets import Static
from textual.widgets import Button
from textual.containers import Vertical

from core.RecommendationEngine import RecommendationEngine
from core.AutoDetection import AutoDetectionEngine
from core.ConfigManager import ConfigManager

from Scanner.parallelScan import ParallelScan


class ReportScreen(Screen):

    def __init__(self, results):

        super().__init__()

        self.results = results

        self.config = ConfigManager()

    def compose(self):

        success = 0
        failed = 0

        report = ""

        report += "Cleaning Report\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        for cache, status in self.results.items():

            if status:

                report += f"✓ {cache}\n"

                success += 1

            else:

                report += f"✗ {cache}\n"

                failed += 1

        report += "\n"

        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        report += f"Success : {success}\n"

        report += f"Failed  : {failed}\n"

        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        scanResults = ParallelScan()

        # -----------------------------
        # Recommendation Engine
        # -----------------------------

        if self.config.get("showRecommendation"):

            report += "\nRecommendations\n\n"

            try:

                recommendationEngine = RecommendationEngine()

                recommendations = recommendationEngine.generate(
                    scanResults
                )

                if recommendations:

                    for item in recommendations:

                        report += f"✓ {item}\n"

                else:

                    report += "✓ No recommendations.\n"

            except Exception:

                report += "Recommendation Engine unavailable.\n"

        # -----------------------------
        # Auto Detection
        # -----------------------------

        if self.config.get("showAutoDetection"):

            report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

            report += "\nAuto Detection\n\n"

            try:

                detectionEngine = AutoDetectionEngine()

                warnings = detectionEngine.analazye(
                    scanResults
                )

                if warnings:

                    for item in warnings:

                        report += (

                            f"⚠ "

                            f"{item['title']} "

                            f"[{item['level']}] : "

                            f"{item['message']}\n"

                        )

                else:

                    report += "✓ No issues detected.\n"

            except Exception as e:

                report += f"Auto Detection Error : {e}\n"

        yield Header()

        yield Vertical(

            Static(

                report,

                id="report"

            ),

            Button(

                "Back To Menu",

                id="back"

            )

        )

        yield Footer()

    def on_button_pressed(self, event):

        if event.button.id == "back":

            self.app.pop_screen()

            self.app.pop_screen()