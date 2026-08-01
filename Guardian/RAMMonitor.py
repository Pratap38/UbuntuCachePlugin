#memory se data collect kr rha yaha se

from datetime import datetime
import psutil
from Guardian.models.MemoryInfo import MemoryInfo
class RamMonitor:
    def __init__(self):
        self.virtualmemory=None
        self.swapMemory=None

    def refresh(self):
        self.virtualmemory=psutil.virtual_memory()
        self.swapMemory=psutil.swap_memory()
    def collect(self)->MemoryInfo:                         ##function for latest memory info
        self.refresh()
        return MemoryInfo(
            timestamp=datetime.now(),
            totalRam=self.virtualmemory.total,
            availableRam=self.virtualmemory.available,
            usedRam=self.virtualmemory.used,
            freeRam=self.virtualmemory.free,
            cacheRam=getattr(
                self.virtualmemory,
                "cached",
                0
            ),
            bufferRam=getattr(
                self.virtualmemory,
                "buffer",
                0
            ),
            ramPercent=self.virtualmemory.percent,
            totalSwap=self.swapMemory.total,
            usedSwap=self.swapMemory.used,
            freeSwap=self.swapMemory.free,
            swapPercent=self.swapMemory.percent
        )
    def RamUsage(self)->float:
        return self.collect().ramPercent
    def swapPercent(self)->float:
        return self.collect().swapPercent
    def AvailableRam(self)->int:
        return self.collect().availableRam
    def HasSwap(self)->bool:
        return self.collect().hasSwap
    def UsingSwap(self)->bool:
        return self.collect().usedSwap>0



    
    def get_memory_info(self)->MemoryInfo:
        pass
    def usage_percent(self)->float:
        pass
    def available_ram(self)->int:
        pass
    def swapUsage(self)->float:
        pass
