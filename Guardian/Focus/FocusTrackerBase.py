from abc import ABC, abstractmethod

from Guardian.models.WindowInfo import WindowInfo


class FocusTracker(ABC):

    @abstractmethod
    def getActiveWindow(self) -> WindowInfo | None:
        pass

    @abstractmethod
    def getFocusedApplication(self) -> str | None:
        pass

    @abstractmethod
    def isSupported(self) -> bool:
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass