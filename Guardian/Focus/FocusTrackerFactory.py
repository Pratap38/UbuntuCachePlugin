from Guardian.DesktopChecker import DesktopChecker
from Guardian.models.DesktopEnvironment import DesktopEnv
from Guardian.Focus.FocusTrackerBase import FoucuTracker
from Guardian.Focus.FocusTrackerWayland import FocusTrackerWayland

class FocusTrackerFactory:
    @staticmethod
    def create(environment:DesktopEnv|None=None,)->FoucuTracker:
        if environment is None:
            environment=DesktopChecker().current()
        if environment==DesktopEnv.WAYLAND:
            return FocusTrackerWayland()
        if environment==DesktopEnv.x11:
            return NotImplementedError(
                "X11 is currently not implement is in devlopiing phase"
            )
        raise RuntimeError(
            "Unsupported desktop environment: "
            f"{environment}"
        )
