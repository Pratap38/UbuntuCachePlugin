import psutil
import os 
import signal
from Guardian.WhitelistManager import WhitelistManager




class PauseManager:

    def __init__(self,whitelistManager=None):
        self.whitelistManager=(
            whitelistManager
            or WhitelistManager()
        )

    def canpause(self,pid:int)->bool:
        if pid<=0:
            return False
        try:
            process=psutil.Process(pid)

            if not process.is_running():
                return False
            currentUser=psutil.Process(
                os.getpid()
            ).username()

            processuser=process.username()
            if processuser!=currentUser:
                return False

            if self.whitelistManager.isWhitelistedName(process.name()):
                return False
            if pid==os.getpid():
                return False
            return True
        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                return False

    def pause(self, pid: int) -> bool:

        if not self.canpause(pid):
            return False

        try:

            os.kill(
                pid,
                signal.SIGSTOP
            )

            return True

        except (
            ProcessLookupError,
            PermissionError,
            OSError,
        ):
            return False
    def resume(self,pid:int)->bool:
        try:
            process=psutil.Process(pid)

            if not process.is_running():
                return False

            os.kill(
                pid,
                signal.SIGCONT
            )
            return True
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
            ProcessLookupError,
            PermissionError,
            OSError,
        ):
            return False
    def isPaused(self, pid: int) -> bool:

        try:

            process = psutil.Process(pid)

            return process.status() == psutil.STATUS_STOPPED

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return False