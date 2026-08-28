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