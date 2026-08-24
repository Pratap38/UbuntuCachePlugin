from Guardian.GuardianConfig import GuardianConfig

class ResumePolicy:
    def __init__(self):
        self.config=GuardianConfig()
        self.resumeThreshold=self.config.get("resumeThreshold",75)
    def canResume(self,ramPercent:float)->bool:
        if ramPercent<0:
            return False
        if ramPercent>100:
            return False
        return ramPercent<=self.resumeThreshold

    def threshold(self)->float:
        return self.resumeThreshold
