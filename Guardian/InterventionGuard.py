import time


class InterventionGuard:

    def __init__(
        self,
        cooldownSeconds: float = 30.0,
        maxInterventions: int = 1
    ):

        if cooldownSeconds < 0:
            raise ValueError(
                "Cooldown cannot be negative."
            )

        if maxInterventions < 1:
            raise ValueError(
                "Maximum interventions must be at least 1."
            )

        self.cooldownSeconds = cooldownSeconds
        self.maxInterventions = maxInterventions

        self.interventionCount = 0
        self.lastInterventionTime = None


    def canIntervene(self) -> bool:

        if (
            self.interventionCount
            >= self.maxInterventions
        ):
            return False

        if self.lastInterventionTime is None:
            return True

        elapsed = (
            time.monotonic()
            - self.lastInterventionTime
        )

        return elapsed >= self.cooldownSeconds

    

    def recordIntervention(self):

        self.interventionCount += 1

        self.lastInterventionTime = (
            time.monotonic()
        )

   
    def reset(self):

        self.interventionCount = 0
        self.lastInterventionTime = None

    # --------------------------------------------------
    # Remaining interventions
    # --------------------------------------------------

    def remainingInterventions(self) -> int:

        return max(
            0,
            self.maxInterventions
            - self.interventionCount
        )