import time
from typing import Optional

from Guardian.GuardianOrchestrator import GuardianOrchestrator


class GuardianEngine:

    def __init__(
        self,
        orchestrator: Optional[GuardianOrchestrator] = None,
        interval: float = 5.0,
    ):

        if interval <= 0:
            raise ValueError(
                "Guardian interval must be greater than zero."
            )

        self.orchestrator = (
            orchestrator
            if orchestrator is not None
            else GuardianOrchestrator()
        )

        self.interval = interval

        self.running = False

        self.notificationManager = (
            self.orchestrator.notificationManager
        )

   

    def start(self):

        if self.running:
            return

        self.running = True

        try:

            while self.running:

                self.runCycle()

                if not self.running:
                    break

                time.sleep(
                    self.interval
                )

        finally:

            self.running = False

    

    def stop(self):

        self.running = False

    

    def runCycle(self):

        memory = (
            self.orchestrator.ramMonitor.collect()
        )

        pressure = (
            self.orchestrator.pressureCheck.analyze(
                memory
            )
        )

        decision = (
            self.orchestrator.decisionEngine.decide(
                pressure
            )
        )

        notificationSent = (
            self.notificationManager.notify(
                pressure,
                memory.ramPercent
            )
        )

        return {
            "memory": memory,
            "pressure": pressure,
            "decision": decision,
            "notificationSent": notificationSent,
        }