from Guardian.models.ProcessInfo import ProcessInfo

class MemoryRanker:
    def rank(
            self,
            processes:list[ProcessInfo]
    )->list[ProcessInfo]:
        if not processes:
            return[]
        return sorted(processes,key=lambda process:process.memoryBytes,
                      reverse=True)


    def topdetail(
            self,processes:list[ProcessInfo],limit:int =10
    )->list[ProcessInfo]:
        if limit<=0:
            return[]
        ranked=self.rank(processes)

        return ranked[:limit]
    