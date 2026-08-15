##ab process tracker ka code bana rhe ki current applcation konse runing me hai 

import psutil
from Guardian.models.ProcessInfo import ProcessInfo
from Guardian.GuardianConfig import GuardianConfig


class ProcessTracker:
    def runningProcess(self)->list[ProcessInfo]:
        processes=[]
        for process in psutil.process_iter(            ##process iter psutil me method hai through which i can iterate thjough all the process runing in the active terminal 
            ["pid", "name", "username", "memory_info", "memory_percent", "status"]
        ):
            try:
                info=process.info
                memoryInfo=info.get("memory_info")
                if memoryInfo is None:
                    continue
                processInfo=ProcessInfo(
                    pid=info["pid"],
                    name=info.get("name") or "Unknown",
                    userName=info.get("username"),
                    memoryBytes=memoryInfo.rss,
                    memoryPercent=info.get("memory_percent", 0.0),
                    status=info.get("status", "unknown"),
                )
                processes.append(processInfo)
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return processes
         
    def userProcess(self) -> list[ProcessInfo]:

        config = GuardianConfig()

        currentUser = psutil.Process().username()

        whitelist = config.get(
            "whitelist",
            []
        )

        processes = []

        for process in self.runningProcess():

            if process.userName != currentUser:
                continue

            if process.name in whitelist:
                continue

            processes.append(process)

        return processes
    def process(self,pid:int)->ProcessInfo|None:
        try:
            process=psutil.Process(pid)
            memoryInfo=process.memory_info()
            return ProcessInfo(
                pid=process.pid,
                name=process.name(),
                userName=process.username(),
                memoryBytes=memoryInfo.rss,
                memoryPercent=process.memory_percent(),
                status=process.status(),
            )
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):

            return None