##screen pe kya dikh rha



import os
from Guardian.models.DesktopEnvironment import DesktopEnv

class DesktopChecker:
    def __init__(self):
        self.environment=self.detect()
    def detect(self)->DesktopEnv:
        session=os.environ.get(
            "XDG_SESSION_TYPE",

            ""
        ).lower()
        if session=="x11":
            return DesktopEnv.x11
        if session=="wayland":
            return DesktopEnv.WAYLAND
        if os.environ.get("WAYLAND_Display"):
            return DesktopEnv.WAYLAND
        if os.environ.get("DISPLAY"):
            return DesktopEnv.x11
        return DesktopEnv.UNKNOWN
    def current(self)->DesktopEnv:
        return self.environment
    
    def isX11(self) -> bool:

        return self.environment == DesktopEnv.x11

    # -----------------------------------------------------

    def isWayland(self) -> bool:

        return self.environment == DesktopEnv.WAYLAND

    # -----------------------------------------------------

    def isUnknown(self) -> bool:

        return self.environment == DesktopEnv.UNKNOWN

    # -----------------------------------------------------

    def supportsWindowTracking(self) -> bool:
        """
        Returns whether Guardian can use
        X11-based window tools.
        """

        return self.environment.supportwindowTrack