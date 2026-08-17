from datetime import datetime
class LRU:

    def __init__(self):
        self.lastUsed={}
    def update(self,pid:int,
               timestamp:datetime|None=None)->None:
        if pid<=0:
            return
        if timestamp is None:
            timestamp=datetime.now()
        self.lastUsed[pid]=timestamp
    def leastRecent(self)->list[int]:
        return[
            pid
            for pid,_ in sorted(
                self.lastUsed.items(),
                key=lambda item:item[1]
            )
        ]

##simope==ke same step fr most recent just reverse the least recent work

    def mostRecent(self)->list[int]:
        return[
            pid
            for pid,_ in sorted(
                self.lastUsed.items(),
                key=lambda item:item[1],
                reverse=True
            )
        ]

    def getLastUsed(self,pid:int)->datetime|None:
        return self.lastUsed.get(pid)

    def remove(self,pid:int)->None:
        self.lastUsed.pop(pid,None)


    def clear(self)->None:
        self.lastUsed.clear()

    def size(self)->int:
        return len(self.lastUsed)
    def updateFromWindow(self, window) -> None:

        if window is None:
            return

        if not window.isValid:
            return

        if not window.focused:
            return

        self.update(
            window.pID,
            window.timestamp
        )