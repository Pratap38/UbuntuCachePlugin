from datetime import datetime

from Guardian.Focus.FocusTrackerBase import FoucuTracker
from Guardian.models.WindowInfo import WindowInfo
from Guardian.models.DesktopEnvironment import DesktopEnv

from Guardian.platform.Wayland.WindowDetector import WindowDetector
from Guardian.platform.Wayland.ApplicationResolver import ApplicationPauseContinue


class FocusTrackerWayland(FoucuTracker):

    def __init__(self):

        self.detector = WindowDetector()

        self.resolver = ApplicationPauseContinue()

        self.currentWindow = None

    # -----------------------------------------------------

    def getActiveWindow(self) -> WindowInfo:

        detected = self.detector.detect()

        if detected is None:

            return None

        application = detected.get(

            "application",

            "Unknown"

        )

        title = detected.get(

            "title",

            "Unknown Window"

        )

        pid = self.resolver.resolvepid(

            application

        )

        self.currentWindow = WindowInfo(
            windoId=detected.get("window_id", "WAYLAND"),
            pID=pid or -1,
            application=application,
            title=title,
            focused=True,
            timestamp=datetime.now(),
            environment=DesktopEnv.WAYLAND,
        )

        return self.currentWindow

    # -----------------------------------------------------

    def getFocusedApplication(self):

        window = self.getActiveWindow()

        if window:

            return window.application

        return None

    # -----------------------------------------------------

    def isSupported(self):

        return self.detector.supportDetector()

    # -----------------------------------------------------

    def refresh(self):

        self.currentWindow = self.getActiveWindow()
