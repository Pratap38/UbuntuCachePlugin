from Guardian.DecisionEngine import DecisionEngine
from Guardian.models.PressureState import PressureState


def run_test():

    print("\n========== Decision Engine Test ==========\n")

    engine = DecisionEngine()

    # --------------------------------------------------
    # NORMAL
    # --------------------------------------------------

    print("Testing NORMAL state...")

    decision = engine.decide(
        PressureState.NORMAL
    )

    assert decision is False

    print("NORMAL → NO ACTION")
    print("PASS")

    # --------------------------------------------------
    # WARNING
    # --------------------------------------------------

    print("\nTesting WARNING state...")

    decision = engine.decide(
        PressureState.WARNING
    )

    assert decision is False

    print("WARNING → NO ACTION")
    print("PASS")

    # --------------------------------------------------
    # CRITICAL
    # --------------------------------------------------

    print("\nTesting CRITICAL state...")

    decision = engine.decide(
        PressureState.CRITICAL
    )

    assert decision is True

    print("CRITICAL → ACTION REQUIRED")
    print("PASS")

    # --------------------------------------------------
    # EMERGENCY
    # --------------------------------------------------

    print("\nTesting EMERGENCY state...")

    decision = engine.decide(
        PressureState.EMERGENCY
    )

    assert decision is True

    print("EMERGENCY → ACTION REQUIRED")
    print("PASS")

    # --------------------------------------------------

    print("\n==========================================")

    print("\nDECISION ENGINE TEST PASSED\n")


if __name__ == "__main__":

    run_test()