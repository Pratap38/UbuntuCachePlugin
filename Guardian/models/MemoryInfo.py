from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class MemoryInfo:
    timestamp:datetime

    #physical ram information
    totalRam:int
    availableRam:int
    usedRam:int
    freeRam:int
    cacheRam:int
    bufferRam:int
    ramPercent:float

    #swapp memory information
    totalSwap:int
    usedSwap:int
    freeSwap:int
    swapPercent:float

    @property
    def totalRamGb(self)->float:
        return round(self.totalRam/(1024**3),2)

    @property
    def availableRamGb(self)->float:
        return round(self.availableRam/(1024**3),2)

    @property
    def usedRamGb(self)->float:
        return round(self.usedRam/(1024**3),2)
    @property
    def freeRamGb(self)->float:
        return round(self.freeRam/(1024**3),2)
    @property
    def cacheRamGb(self)->float:
        return round(self.cacheRam/(1024**3),2)
    @property
    def bufferRamGb(self)->float:
        return round(self.bufferRam/(1024**3),2)
    @property
    def totalSwapGb(self)->float:
        return round(self.totalSwap/(1024**3),2)
    @property
    def usedSwapGb(self)->float:
        return round(self.usedSwap/(1024**3),2)
    @property
    def freeSwapGb(self)->float:
        return round(self.freeSwap/(1024**3),2)


    def hasSwap(self)->bool:
        return self.totalSwap>0
    def memoryPressure(self)->float:
        return self.ramPercent
    def swapPressure(self)->float:
        return self.swapPercent
    def toDictionary(self)->dict:

            return {
                "timestamp": self.timestamp.isoformat(),

                "totalRam": self.totalRam,
                "availableRam": self.availableRam,
                "usedRam": self.usedRam,
                "freeRam": self.freeRam,

                "cacheRam": self.cacheRam,
                "bufferRam": self.bufferRam,

                "ramPercent": self.ramPercent,

                "totalSwap": self.totalSwap,
                "usedSwap": self.usedSwap,
                "freeSwap": self.freeSwap,

                "swapPercent": self.swapPercent
            }

    def __str__(self) -> str:
            """
            Human-readable representation.
            """
            return (
                f"MemoryInfo("
                f"RAM={self.usedRamGb}/{self.totalRamGb} GB "
                f"({self.ramPercent:.1f}%), "
                f"Swap={self.usedSwapGb}/{self.totalSwapGb} GB "
                f"({self.swapPercent:.1f}%)"
                f")"
            )
