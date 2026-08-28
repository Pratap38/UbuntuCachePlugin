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
import datetime
from Guardian.models.GuardianEvent import GuardianEvent
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
    def pauseCandidate(self,process,rampercent:float,reason:str="RAM Critical")->bool:
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
            ramPercent=rampercent
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

        
        