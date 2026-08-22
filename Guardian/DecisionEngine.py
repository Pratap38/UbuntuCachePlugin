from Guardian.models.PressureState import PressureState


class DecisionEngine:

    def decide(
        self,
        pressureState: PressureState
    ) -> bool:

        return pressureState.RequireAction()