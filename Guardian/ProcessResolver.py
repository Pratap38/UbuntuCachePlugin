import psutil

from Guardian.models.ProcessInfo import ProcessInfo

class ProcessResolve:
    def resolve(self,
                pid:int)->ProcessInfo|None:
        if pid<=0:
            return None
        try:
            process=psutil.Process(pid)
            memory=process.memory_info()

            return ProcessInfo(
               pid=process.pid,
                name=process.name(),
                userName=process.username(),
                memoryBytes=memory.rss,
                memoryPercent=process.memory_percent(),
                status=process.status(),

            )
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):

            return None