from Guardian.GuardianConfig import GuardianConfig
from models.PressureState import PressureState
from models.MemoryInfo import MemoryInfo


class MemoryPressureCheck:
    def __init__(self):
        self.config=GuardianConfig()

        def analyze(
                self,
                memory:MemoryInfo
        )->PressureState:
            ramUsage=memory.ramPercent
            emergency=self.config.get(
                "emergencyThreshold"
            )
            critical=self.config.get(
                "criticalThreshold"
            )
            warning=self.config.get(
                "warningThreshold"
            )
            if ramUsage>=emergency:
                return PressureState.EMERGENCY
            elif ramUsage>=critical:
                return PressureState.CRITICAL
            elif ramUsage>=warning:
                return PressureState.WARNING
            return PressureState.NORMAL
        def isNormal(self,memory:MemoryInfo)->bool:
            return(self.analyze(memory)==PressureState.NORMAL)
        def isWarning(self,memory:MemoryInfo)->bool:
            return(self.analyze(memory)==PressureState.WARNING)
        def isCritical(self,memory:MemoryInfo)->bool:
                    return(self.analyze(memory)==PressureState.CRITICAL)
        def isEmergency(self,memory:MemoryInfo)->bool:
                    return(self.analyze(memory)==PressureState.EMERGENCY)
        
                