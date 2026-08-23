import subprocess
from Guardian.models.PressureState import PressureState

class NotificationManager:
    def __init__(self):
        self.lastState=None
    def send(
        self,
        title: str,
        message: str,
        urgency: str = "normal"
    ) -> bool:

        try:

            result = subprocess.run(
                [
                    "notify-send",
                    "--urgency",
                    urgency,
                    title,
                    message
                ],
                capture_output=True,
                text=True
            )

            return result.returncode == 0

        except (
            FileNotFoundError,
            OSError
        ):
            return False
    def notify(
        self,
        state: PressureState,
        ramPercent: float
    ) -> bool:

        if state == PressureState.NORMAL:

            return False

        if state == PressureState.WARNING:

            return self.send(
                "RAM Guardian — Warning",
                (
                    f"RAM usage is {ramPercent:.1f}%. "
                    "Memory usage is increasing."
                ),
                "normal"
            )

        if state == PressureState.CRITICAL:

            return self.send(
                "RAM Guardian — Critical Memory",
                (
                    f"RAM usage has reached "
                    f"{ramPercent:.1f}%. "
                    "RAM Guardian may need to pause a process."
                ),
                "critical"
            )

        if state == PressureState.EMERGENCY:

            return self.send(
                "RAM Guardian — Emergency",
                (
                    f"RAM usage is critically high "
                    f"at {ramPercent:.1f}%. "
                    "Immediate memory protection may be required."
                ),
                "critical"
            )

        return False

    def earlyWarning(
        self,
        ramPercent: float,
        threshold: float = 85.0
    ) -> bool:

        if ramPercent < threshold:

            return False

        return self.send(
            "RAM Guardian — Early Warning",
            (
                f"RAM usage is {ramPercent:.1f}%. "
                f"Critical threshold is approaching "
                f"({threshold:.0f}% early warning)."
            ),
            "normal"
        )     