from dataclasses import  dataclass
from datetime import datetime

@dataclass(slots=True)
class PauseProcess:
    pid: int
    name: str
    pausedAt: datetime
    reason: str
    processStartTime: float

    def __str__(self)->str:
        return (
            f"PausedProcess("
            f"pid={self.pid}, "
            f"name={self.name}, "
            f"reason={self.reason}, "
            f"pausedAt={self.pausedAt}"
            f")"
        )
    def toDict(self) -> dict:

        return {
            "pid": self.pid,
            "name": self.name,
            "paused_at": self.pausedAt.isoformat(),
            "reason": self.reason,
        }
        