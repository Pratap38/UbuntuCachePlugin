from dataclasses import dataclass
from datetime import datetime
from Guardian.models.DesktopEnvironment import DesktopEnv


@dataclass
class WindowInfo:
    windoId: str
    pID: int
    application: str
    title: str
    focused: bool
    timestamp: datetime
    environment: DesktopEnv

    def __str__(self):
        return f"{self.application} ({self.title})"

    @property
    def isValid(self):
        return (
            self.windoId != ""
            and self.pID > 0
        )

    @property
    def ageSecond(self):
        return (datetime.now() - self.timestamp).total_seconds()

    def toDict(self):
        return {
            "window_id": self.windoId,
            "pid": self.pID,
            "application": self.application,
            "title": self.title,
            "focused": self.focused,
            "timestamp": self.timestamp.isoformat(),
            "environment": str(self.environment),
        }