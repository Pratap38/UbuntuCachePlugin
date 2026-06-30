import shutil
from core.utils import bytes_to_mb


class AutoDetectionEngine:
    def __init__(self):
        self.alerts=[]
    def addAlert(self,title,level,message):
        self.alerts.append({
            "title": title,
            "level":level,
            "message":message
        })
    def analazye(self,result):
        self.alerts.clear()
        self.checkDiskSpace()
        self.LargeCacheFiles(result)
        return self.alerts
    
    def checkDiskSpace(self):
        total,used,free=shutil.disk_usage("/")
        freeGB=free/(1024**3)
        if freeGB<5:
            self.addAlert(
                "Disk Space",
                "Critical",
                f"Only {freeGB:2f}GB Free"
            )
        elif freeGB<15:
           self.addAlert(
                "Disk Space",
                "Warning ",
                f"Disk Space is Running low {freeGB:2f}GB Free"
            )
        else:

            self.addAlert(

                "Disk Space",

                "Info",

                f"{freeGB:.2f} GB available."

            )
    def LargeCacheFiles(self,result):
        for category in result:
            sizeMB=bytes_to_mb(category.size)
            if sizeMB > 2048:

                self.addAlert(

                    category.name,

                    "Critical",

                    f"{category.name} is using {sizeMB:.2f} MB."

                )

            elif sizeMB > 1024:

                self.addAlert(

                    category.name,

                    "Warning",

                    f"{category.name} is using {sizeMB:.2f} MB."

                )
