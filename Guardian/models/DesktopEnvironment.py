from enum import Enum,auto

class DesktopEnv(Enum):
    x11=auto()
    WAYLAND=auto()
    UNKNOWN=auto()
    def __str__(self):
        if self==DesktopEnv.x11:
            return "X11"
        elif self==DesktopEnv.WAYLAND:
            return "Wayland"
        return "UnKnown"
    @property
    def Description(self):
        description={
            DesktopEnv.x11:
            "Traditional Linux display server",
            DesktopEnv.WAYLAND:
            "Mordern  secure Linux  display protocol",
            DesktopEnv.UNKNOWN:
            "Desktop env  not been detected"
        }
        return description[self]
    @property
    def supportwindowTrack(self):
        return self in (
            DesktopEnv.x11,
            DesktopEnv.WAYLAND,
        )