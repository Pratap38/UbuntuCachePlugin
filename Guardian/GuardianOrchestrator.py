from Guardian.RAMMonitor import RamMonitor
from Guardian.MemoryPressureDetector import MemoryPressureCheck
from Guardian.DecisionEngine import DecisionEngine
from Guardian.CandidateSelector import CandidateSelect
from Guardian.MemoryRanker import MemoryRanker
from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager
from Guardian.PauseRegistry import PauseRegistry
from Guardian.ResumePolicy import ResumePolicy
from Guardian.EventHistory import EventHistory
from Guardian.NotificationManager import NotificationManager
from Guardian.models.PausedProcess import PauseProcess
from datetime import datetime
from Guardian.models.GuardianEvent import GuardianEvent
from Guardian.ResumeCandidateSelector import ResumeCandidateSelector
class GuardianOrchestrator:
    def __init__(self):
        self.ramMonitor=RamMonitor()

        self.pressureCheck=MemoryPressureCheck()
        self.decisionEngine=DecisionEngine()
        self.candidateSelector=CandidateSelect()
        self.memoryRanker=MemoryRanker()
        self.pauseManager=PauseManager()
        self.resumeManager=ResumeManager()
        self.pauseRegistry=PauseRegistry()
        self.resumePolicy=ResumePolicy()
        self.eventHistory=EventHistory()
        self.notificationManager=NotificationManager()

#scan the machine memory info
    def analyzeMemory(self):
        memory=self.ramMonitor.collect()
        pressure=self.pressureCheck.analyze(memory)
        decision=self.decisionEngine.decide(pressure)
        return memory,pressure,decision
## select the specific candidate in order to take the decision action
    def getCandidate(self):
        memory,pressure,decision=self.analyzeMemory()
        if not decision:
            return memory,pressure,decision,[]
        candidate=self.candidateSelector.getCandidates()

        return memory,pressure,decision,candidate
## sortng the candindate on the basis of rht the rank
    def rankCandidate(self):
        memory,pressure,decision,candidate=(self.getCandidate())
        if not decision:
            return memory,pressure,decision,[]
        rank=self.memoryRanker.rank(candidate)
        return memory,pressure,decision,rank
##creating pause marnager in order to now start pausein the app
    def pauseCandidate(self,process,ramPercent:float,reason:str="RAM Critical")->bool:
        if process is None:
            return False
        if process.pid<=0:
            return False
        if not process.name:
            return False
        if process.memoryBytes<=0:
            return False
        if self.pauseRegistry.contains(process.pid):
            return False

        if not self.pauseManager.canpause(process.pid):
            try:
                self.resumeManager.resume(process.pid)
            except Exception:
                pass
            return False

        if not self.pauseManager.pause(process.pid):
            return False

        pauseAt=datetime.now()
        pausedProcess=PauseProcess(
            pid=process.pid,
            name=process.name,
            pausedAt=pauseAt,
            reason=reason
        )
        if not self.pauseRegistry.add(
            pausedProcess
        ):
            try:
                self.resumeManager.resume(
                    process.pid
                )
            except Exception:
                pass

            return False
        event = GuardianEvent(
            eventType="PAUSED",
            pid=process.pid,
            processName=process.name,
            timestamp=pauseAt,
            reason=reason,
            ramPercent=ramPercent
        )

        if not self.eventHistory.add(
            event
        ):
            self.pauseRegistry.remove(
                process.pid
            )

            try:
                self.resumeManager.resume(
                    process.pid
                )
            except Exception:
                pass

            return False

        return True

    def runPauseCycle(self):

        memory = self.ramMonitor.collect()

        pressure = self.pressureCheck.analyze(
            memory
        )

        decision = self.decisionEngine.decide(
            pressure
        )

        if not decision:

            return {
                "action": False,
                "reason": "No action required",
                "memory": memory,
                "pressure": pressure,
                "process": None,
            }

        candidates = self.candidateSelector.getCandidates()

        if not candidates:

            return {
                "action": False,
                "reason": "No eligible candidates",
                "memory": memory,
                "pressure": pressure,
                "process": None,
            }

        ranked = self.memoryRanker.rank(
            candidates
        )

        if not ranked:

            return {
                "action": False,
                "reason": "No ranked candidates",
                "memory": memory,
                "pressure": pressure,
                "process": None,
            }

        for candidate in ranked:

            if self.pauseRegistry.contains(
                candidate.pid
            ):
                continue

            if not self.pauseManager.canpause(
                candidate.pid
            ):
                continue

            success = self.pauseCandidate(
                candidate,
                ramPercent=memory.ramPercent,
                reason="RAM Critical"
            )

            if success:

                return {
                    "action": True,
                    "reason": "Process paused",
                    "memory": memory,
                    "pressure": pressure,
                    "process": candidate,
                }

        return {
            "action": False,
            "reason": "No candidate passed final safety checks",
            "memory": memory,
            "pressure": pressure,
            "process": None,
        }
    def findResumCandidate(self):
        memory=self.ramMonitor.collect()
        selector=ResumeCandidateSelector(pauseRegistry=self.pauseRegistry,resumePolicy=self.resumePolicy)
        candidates=selector.select(memory.ramPercent)

        return (memory,candidates)

        


        