from enum import Enum,auto

class PressureState(Enum):                    # this is used for basically convert kar rhe apan ram ke percentage ko 
                                              ## normal criical medium me
    NORMAL = auto()

    WARNING = auto()

    CRITICAL = auto()

    EMERGENCY = auto()


    def __str__(self)->str:
        return self.name.capitalize()
    @property
    def Description(self)->str:
        description={
            PressureState.NORMAL:
         "System memeory health is normal",
            PressureState.WARNING:
            "Memory Usage Increase",
            PressureState.CRITICAL:
            "Memory usage is critically",
            PressureState.EMERGENCY:
            "System is eraching it limit chances of freezing"
            
        }
        return description[self]
    @property
    def color(self)->str:
        colors = {

            PressureState.NORMAL:
                "green",

            PressureState.WARNING:
                "yellow",

            PressureState.CRITICAL:
                "orange3",

            PressureState.EMERGENCY:
                "red"

        }

        return colors[self]
    @property
    def icon(self)->str:
        icons = {

            PressureState.NORMAL:
                "🟢",

            PressureState.WARNING:
                "🟡",

            PressureState.CRITICAL:
                "🟠",

            PressureState.EMERGENCY:
                "🔴"

        }

        return icons[self]
    def RequireAction(self)->bool:
        return self in(
            PressureState.CRITICAL,
            PressureState.EMERGENCY
        )

                                