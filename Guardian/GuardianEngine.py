import time
from typing import Optional

from Guardian.GuardianOrchestrator import GuardianOrchestrator


from Guardian.InterventionGuard import InterventionGuard


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
        self.interventionGuard = InterventionGuard(
    cooldownSeconds=30.0,
    maxInterventions=1
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

        memory = self.orchestrator.ramMonitor.collect()

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

        pausedProcess = None
        actionTaken = False
        actionReason = "No action required"

        if decision:

            if not self.interventionGuard.canIntervene():

                actionReason = (
                    "Intervention blocked by safety guard"
                )

            else:

                candidates = (
                    self.orchestrator.candidateSelector
                    .getCandidates()
                )

                ranked = (
                    self.orchestrator.memoryRanker
                    .rank(candidates)
                )

                for candidate in ranked:

                    if (
                        self.orchestrator.pauseRegistry
                        .contains(candidate.pid)
                    ):
                        continue

                    if not (
                        self.orchestrator.pauseManager
                        .canPause(candidate.pid)
                    ):
                        continue

                    success = (
                        self.orchestrator.pauseCandidate(
                            candidate,
                            ramPercent=memory.ramPercent,
                            reason="RAM Critical"
                        )
                    )

                    if success:

                        self.interventionGuard.recordIntervention()

                        pausedProcess = candidate

                        actionTaken = True

                        actionReason = (
                            "Process paused"
                        )

                        break

                if pausedProcess is None:

                    actionReason = (
                        "No safe candidate available"
                    )

        return {
            "memory": memory,
            "pressure": pressure,
            "decision": decision,
            "notificationSent": notificationSent,
            "actionTaken": actionTaken,
            "actionReason": actionReason,
            "pausedProcess": pausedProcess,
        }