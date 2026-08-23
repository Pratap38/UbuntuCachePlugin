## this will store the data means the log which app pause which aap resumme creating and hostory to been seen by the user and teh syststyem 
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class GuardianEvent:

    eventType: str
    pid: int
    processName: str
    timestamp: datetime
    reason: str
    ramPercent: float

    def __str__(self) -> str:

        return (
            f"{self.timestamp} | "
            f"{self.eventType} | "
            f"{self.processName} | "
            f"PID={self.pid} | "
            f"RAM={self.ramPercent:.1f}% | "
            f"{self.reason}"
        )

    def toDict(self) -> dict:

        return {
            "event_type": self.eventType,
            "pid": self.pid,
            "process_name": self.processName,
            "timestamp": self.timestamp.isoformat(),
            "reason": self.reason,
            "ram_percent": self.ramPercent,
        }