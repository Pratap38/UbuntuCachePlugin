import os
import psutil
import signal
from Guardian.WhitelistManager import WhitelistManager


class ResumeManager:
    def __init__(self, whitelistManager=None):

        self.whitelistManager = (
            whitelistManager
            or WhitelistManager()
        )
    def canResume(self, pid: int) -> bool:

        if pid <= 0:
            return False

        try:

            process = psutil.Process(pid)

            if not process.is_running():
                return False

          
            currentUser = psutil.Process(
                os.getpid()
            ).username()

            processUser = process.username()

            if processUser != currentUser:
                return False

            # Process must actually be stopped
            if process.status() != psutil.STATUS_STOPPED:
                return False

            return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return False

    def resume(self, pid: int) -> bool:

        if not self.canResume(pid):
            return False

        try:

            os.kill(
                pid,
                signal.SIGCONT
            )

            return True

        except (
            ProcessLookupError,
            PermissionError,
            OSError,
        ):
            return False
    def isRunning(self, pid: int) -> bool:

        try:

            process = psutil.Process(pid)

            if not process.is_running():
                return False

            return process.status() != psutil.STATUS_STOPPED

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            return False
