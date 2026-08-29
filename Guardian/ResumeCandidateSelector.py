from Guardian.PauseRegistry import PauseRegistry
from Guardian.ResumePolicy import ResumePolicy


class ResumeCandidateSelector:

    def __init__(
        self,
        pauseRegistry=None,
        resumePolicy=None
    ):

        self.pauseRegistry = (
            pauseRegistry
            or PauseRegistry()
        )

        self.resumePolicy = (
            resumePolicy
            or ResumePolicy()
        )

  

    def isCandidate(
        self,
        pid: int,
        ramPercent: float
    ) -> bool:

    
        if pid <= 0:
            return False

       
        if not self.pauseRegistry.contains(pid):
            return False

        if not self.resumePolicy.canResume(
            ramPercent
        ):
            return False

        return True

   

    def select(
        self,
        ramPercent: float
    ):

        if not self.resumePolicy.canResume(
            ramPercent
        ):
            return []

        candidates = []

        for process in self.pauseRegistry.getAll():

            if process is None:
                continue

            if process.pid <= 0:
                continue

            if self.isCandidate(
                process.pid,
                ramPercent
            ):

                candidates.append(process)

        return candidates