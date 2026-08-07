import psutil

class ApplicationPauseContinue:
    def __init__(self):
        pass
    def findProcess(self,application:str):
        application=application.lower()

        for process in psutil.process_iter(
            [
                "pid",
                "name",
                "cmdline"
            ]
        ):
            try:
                name=process.info["name"]or ""
                cmdline=" ".join(
                    process.info["cmdline"] or []

                )
                if (
                    application in name.lower()
                    or 
                    application in cmdline.lower()

                ):
                    return process
            except(
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue
            return None
    #determine return of processId
    def resolvepid(self,application:str):
        process=self.findProcess(application)
        if process:
            return process.pid
        return None

    def isRunning(self,application:str):
        return(
            self.findProcess(
                application
            )
            is not None
        )
    def processInfo(self, application: str):


        process = self.findProcess(

            application

        )

        if process is None:

            return None

        try:

            memory = process.memory_info()

            return {

                "pid": process.pid,

                "name": process.name(),

                "memory_mb":

                    memory.rss

                    /

                    1024

                    /

                    1024,

                "status":

                    process.status()

            }

        except (

            psutil.NoSuchProcess,

            psutil.AccessDenied

        ):

            return None