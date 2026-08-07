from dataclasses import dataclass


@dataclass
class DetectedWindow:

    window_id: str

    application: str

    title: str

    backend: str

    def __str__(self):

        return (

            f"{self.application}"

            f" ({self.title})"

        )

    @property
    def isValid(self):

        return (

            self.window_id != ""

            and

            self.application != ""

        )

    def toDict(self):

        return {

            "window_id": self.window_id,

            "application": self.application,

            "title": self.title,

            "backend": self.backend

        }