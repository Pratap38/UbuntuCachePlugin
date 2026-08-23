# import subprocess
# from Guardian.models.PressureState import PressureState

# class NotificationManager:
#     def __init__(self):
#         self.lastState=None
#     def send(
#         self,
#         title: str,
#         message: str,
#         urgency: str = "normal"
#     ) -> bool:

#         try:

#             result = subprocess.run(
#                 [
#                     "notify-send",
#                     "--urgency",
#                     urgency,
#                     title,
#                     message
#                 ],
#                 capture_output=True,
#                 text=True
#             )

#             return result.returncode == 0

#         except (
#             FileNotFoundError,
#             OSError
#         ):
#             return False
#     def notify(
#         self,
#         state: PressureState,
#         ramPercent: float
#     ) -> bool:

#         if state == PressureState.NORMAL:

#             return False

#         if state == PressureState.WARNING:

#             return self.send(
#                 "RAM Guardian — Warning",
#                 (
#                     f"RAM usage is {ramPercent:.1f}%. "
#                     "Memory usage is increasing."
#                 ),
#                 "normal"
#             )

#         if state == PressureState.CRITICAL:

#             return self.send(
#                 "RAM Guardian — Critical Memory",
#                 (
#                     f"RAM usage has reached "
#                     f"{ramPercent:.1f}%. "
#                     "RAM Guardian may need to pause a process."
#                 ),
#                 "critical"
#             )

#         if state == PressureState.EMERGENCY:

#             return self.send(
#                 "RAM Guardian — Emergency",
#                 (
#                     f"RAM usage is critically high "
#                     f"at {ramPercent:.1f}%. "
#                     "Immediate memory protection may be required."
#                 ),
#                 "critical"
#             )

#         return False

#     def earlyWarning(
#         self,
#         ramPercent: float,
#         threshold: float = 85.0
#     ) -> bool:

#         if ramPercent < threshold:

#             return False

#         return self.send(
#             "RAM Guardian — Early Warning",
#             (
#                 f"RAM usage is {ramPercent:.1f}%. "
#                 f"Critical threshold is approaching "
#                 f"({threshold:.0f}% early warning)."
#             ),
#             "normal"
#         )     


## jsut to avoiud the user fom gettingf spam notication redesing it 
import subprocess

from Guardian.models.PressureState import PressureState


class NotificationManager:

    def __init__(
        self,
        earlyThreshold: float = 85.0
    ):

        self.earlyThreshold = earlyThreshold

        self.earlyWarningSent = False
        self.warningSent = False
        self.criticalSent = False
        self.emergencySent = False

  

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

   

    def earlyWarning(
        self,
        ramPercent: float
    ) -> bool:

        if ramPercent < self.earlyThreshold:

            return False

        if self.earlyWarningSent:

            return False

        result = self.send(
            "RAM Guardian — Early Warning",
            (
                f"RAM usage is {ramPercent:.1f}%. "
                "Critical memory pressure is approaching."
            ),
            "normal"
        )

        if result:

            self.earlyWarningSent = True

        return result

   

    def notify(
        self,
        state: PressureState,
        ramPercent: float
    ) -> bool:

        if state == PressureState.NORMAL:

            self.reset()

            return False

        if state == PressureState.WARNING:

            if self.warningSent:

                return False

            result = self.send(
                "RAM Guardian — Warning",
                (
                    f"RAM usage is {ramPercent:.1f}%. "
                    "Memory usage is increasing."
                ),
                "normal"
            )

            if result:

                self.warningSent = True

            return result

        if state == PressureState.CRITICAL:

            if self.criticalSent:

                return False

            result = self.send(
                "RAM Guardian — Critical Memory",
                (
                    f"RAM usage has reached "
                    f"{ramPercent:.1f}%. "
                    "RAM Guardian may need to pause a process."
                ),
                "critical"
            )

            if result:

                self.criticalSent = True

            return result

        if state == PressureState.EMERGENCY:

            if self.emergencySent:

                return False

            result = self.send(
                "RAM Guardian — Emergency",
                (
                    f"RAM usage is critically high "
                    f"at {ramPercent:.1f}%. "
                    "Immediate memory protection may be required."
                ),
                "critical"
            )

            if result:

                self.emergencySent = True

            return result

        return False

   

    def reset(self) -> None:

        self.earlyWarningSent = False
        self.warningSent = False
        self.criticalSent = False
        self.emergencySent = False