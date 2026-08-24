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
        self.decisonEngine=DecisionEngine()
        self.candidateSelector=CandidateSelect()
        self.memoryRanker=MemoryRanker()
        self.pauseRegister=PauseRegistry()
        self.resumePolicy=ResumePolicy()
        self.eventHistory=EventHistory()
        self.notificationManager=NotificationManager()