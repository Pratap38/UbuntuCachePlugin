# The creation of this file is to showcase the user which file is been unable to delete 

from core.logger import logger

class RecoveryManager:

    def __init__(self):
        self.failedfile=[]
        self.Permissionerror=[]
        self.Lockfile=[]

    def addFailedfile(self,path):
        self.failedfile.append(path)
        logger.warning(f"failed file added {path}")
    def addPermissionerror(self,path):
        self.Permissionerror.append(path)
        logger.warning(f"Perrmission Error added{path} ")
    def addLockfile(self,path):
        self.Lockfile.append(path)
        logger.warning(f"Lockfile erro {path}")
    def TotalsummaryReport(self):
        print("****Total Error Summary****")
        print(f"Total failed file {len(self.failedfile)}")
        print(f"Total Permission Error files {len(self.Permissionerror)}")
        print(f"Total Lockfile {len(self.Lockfile)}")
recoverymanager=RecoveryManager()
