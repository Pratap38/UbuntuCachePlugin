from Guardian.GuardianConfig import GuardianConfig

class WhitelistManager:
    def __init__(self,config=None):
         self.config=config or GuardianConfig()


    def getAll(self)->list[str]:
        whitelist=self.config.get(
            "whitelist",
            []
        )
        return list(whitelist)
    def isWhitelistedName(self,processName:str)->bool:
        if not  processName:
            return False
        return processName in self.getAll()
    def isWhitelisted(
        self,
        process
    ) -> bool:

        if process is None:
            return False

        return self.isWhitelistedName(
            process.name
        )
    def add(
        self,
        processName: str
    ) -> bool:

        if not processName:
            return False

        whitelist = self.getAll()

        if processName in whitelist:
            return False

        whitelist.append(processName)

        self.config.set(
            "whitelist",
            whitelist
        )

        self.config.update()

        return True
    def remove(
        self,
        processName: str
    ) -> bool:

        whitelist = self.getAll()

        if processName not in whitelist:
            return False

        whitelist.remove(processName)

        self.config.set(
            "whitelist",
            whitelist
        )

        self.config.update()

        return True
    def isEmpty(self) -> bool:

        return len(self.getAll()) == 0