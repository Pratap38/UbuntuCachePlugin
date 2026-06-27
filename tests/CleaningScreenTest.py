from textual.app import App

from ui.CleanScreen import CleaningScreen


class TestApp(App):

    def on_mount(self):

        self.push_screen(

            CleaningScreen(

                [

                    "Browser Cache",

                    "Thumbnail Cache",

                    "Trash"

                ]

            )

        )


app = TestApp()

app.run()