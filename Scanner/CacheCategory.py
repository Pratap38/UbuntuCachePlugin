class cacheCategory:
    def __init__(self,name,path,riskLevel="Safe"):
        self.name=name
        self.path=path
        self.riskLevel=riskLevel
        self.size=0
        self.files=0
    def toDict(self):
        return{
            "name":self.name,
            "path":self.path,
            "risk-Level":self.riskLevel,
            "size":self.size,
            "files":self.files
        }