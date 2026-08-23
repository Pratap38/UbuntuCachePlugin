## this will showcase in the ui and log the history of pause and resume
from Guardian.models.GuardianEvent import GuardianEvent


class EventHistory:

    def __init__(
        self,
        limit: int = 100         ##we have setted the lomt p yje log to 100 in order to not create an mess up record
    ):

        self.limit = limit
        self.events: list[GuardianEvent] = []

    
    def add(
        self,
        event: GuardianEvent
    ) -> bool:

        if event is None:
            return False

        if event.pid <= 0:
            return False

        if not event.processName:
            return False

        self.events.append(event)

       
        if len(self.events) > self.limit:

            self.events.pop(0)

        return True

   

    def getAll(
        self
    ) -> list[GuardianEvent]:

        return list(self.events)

    def latest(
        self
    ) -> GuardianEvent | None:

        if not self.events:

            return None

        return self.events[-1]

   

    def forProcess(
        self,
        pid: int
    ) -> list[GuardianEvent]:

        return [
            event
            for event in self.events
            if event.pid == pid
        ]

  

    def count(self) -> int:

        return len(self.events)

  
    def clear(self) -> None:

        self.events.clear()