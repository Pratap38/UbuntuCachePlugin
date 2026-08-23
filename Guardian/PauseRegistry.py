from Guardian.models.PausedProcess import PauseProcess

class PauseRegistry:
    def __init__(self):

        self.processes: dict[int, PauseProcess] = {}

    def add(self,process:PauseProcess)->bool:
        if process is None:
            return False

        if process.pid<=0:
            return False
        if process.pid in self.processes:
            return False
        self.processes[process.pid]=process
        return True


    def remove(self,pid:int)->bool:
        if pid not in self.processes:
            return False
        del self.processes[pid]
        return True
    
    def contains(
        self,
        pid: int
    ) -> bool:

        return pid in self.processes
    def get(
            self,
            pid: int
        ) -> PauseProcess | None:

            return self.processes.get(pid)
    def getAll(
        self
    ) -> list[PauseProcess]:

        return list(
            self.processes.values()
        )
    def count(self) -> int:

        return len(self.processes)
    def clear(self) -> None:

        self.processes.clear()