from datetime import datetime

from Guardian.Focus.FocusTrackerBase import FocusTrackerBase
from Guardian.models.WindowInfo import WindowInfo
from Guardian.models.DesktopEnvironment import DesktopEnvironment


class MockFocusTracker(FocusTrackerBase):

    def __init__(self):

        self.window = WindowInfo(

            window_id="MOCK-0001",

            pid=12345,

            application="Firefox",

            title="ChatGPT - Mozilla Firefox",

            focused=True,

            timestamp=datetime.now(),

            environment=DesktopEnvironment.WAYLAND

        )

    # -----------------------------------------------------

    def getActiveWindow(self) -> WindowInfo:

        return self.window

    # -----------------------------------------------------

    def getFocusedApplication(self) -> str:

        return self.window.application

    # -----------------------------------------------------

    def isSupported(self) -> bool:

        return True

    # -----------------------------------------------------

    def refresh(self) -> None:

        self.window.timestamp = datetime.now()

    # -----------------------------------------------------

    def setWindow(

        self,

        application: str,

        title: str,

        pid: int = 1000

    ):

        """
        Change the active window.

        Useful for testing.
        """

        self.window = WindowInfo(

            window_id=f"MOCK-{pid}",

            pid=pid,

            application=application,

            title=title,

            focused=True,

            timestamp=datetime.now(),

            environment=DesktopEnvironment.WAYLAND

        )