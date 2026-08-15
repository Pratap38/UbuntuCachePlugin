from dataclasses import dataclass

@dataclass(slots=True)
class ProcessInfo:
    pid:int
    name:str
    userName:str|None       ##pratap||root linux user use kar rha

    memoryBytes:int
    memoryPercent:float
    status:str

    @property
    def memoryMb(self)->float:
        return round(
            self.memoryBytes/(1024**2),
            2
        )
    @property
    def memoryGb(self)->float:
        return round(
            self.memoryBytes/(1024**3),
            2
        )
    def __str__(self)->str:
        return(
            f"processInfo("
            f"pid={self.pid},"
            f"name={self.name},"
            f"memory={self.memoryMb} MB,"
            f"status={self.status}"
            f")"
        )
        