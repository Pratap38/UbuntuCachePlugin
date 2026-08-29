from Guardian.ProcessTracker import ProcessTracker
from Guardian.WhitelistManager import WhitelistManager
from Guardian.models.ProcessInfo import ProcessInfo


class CandidateSelect:
    def __init__(self,processTracker=None,whitelistManager=None):
        self.processTracker=(
            processTracker or
            ProcessTracker()
        )
        self.whitelistManager=(
            whitelistManager or 
            WhitelistManager()
        )
    def isCandidate(self,process:ProcessInfo)->bool:
        if process is None:
            return False
        if process.pid<=0:
            return False
        if not process.name:
            return False
        if process.userName is None:
            return False
        if process.memoryBytes <0:
            return False
        if self.whitelistManager.isWhitelisted(process):
            return False
        return True
    def getCandidates(self) -> list[ProcessInfo]:

        candidates = []

        processes = self.processTracker.userProcess()

        for process in processes:

            if self.isCandidate(process):

                candidates.append(process)

        return candidates

    def createFromProcess(self, process) -> ProcessInfo | None:
        try:
            memory = process.memory_info()
            return ProcessInfo(
                pid=process.pid,
                name=process.name(),
                userName=process.username(),
                memoryBytes=memory.rss,
                memoryPercent=process.memory_percent(),
                status=process.status(),
            )
        except Exception:
            return None
        