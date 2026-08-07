from abc import ABC ,abstractmethod
from Guardian.models.WindowInfo import WindowInfo

class FoucuTracker(ABC):

    @abstractmethod
    def getActiveWindow(self) -> WindowInfo:
       
        pass

  

    @abstractmethod
    def getFocusedApplication(self) -> str:
        
        pass
   

    @abstractmethod
    def isSupported(self) -> bool:
      
        pass

    

    @abstractmethod
    def refresh(self) -> None:
        
        pass