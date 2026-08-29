import time

from Guardian.InterventionGuard import (
    InterventionGuard
)


def run_test():

    print(
        "\n========== Intervention Guard Test ==========\n"
    )

    guard = InterventionGuard(
        cooldownSeconds=1.0,
        maxInterventions=2
    )

    # --------------------------------------------------
    # First intervention
    # --------------------------------------------------

    print(
        "Testing initial intervention..."
    )

    assert guard.canIntervene() is True

    print(
        "Initial intervention → ALLOWED"
    )

    print("PASS")

    # --------------------------------------------------
    # Record intervention
    # --------------------------------------------------

    print(
        "\nRecording intervention..."
    )

    guard.recordIntervention()

    assert guard.interventionCount == 1

    print(
        "Intervention count : 1"
    )

    print("PASS")

    # --------------------------------------------------
    # Immediate second intervention
    # --------------------------------------------------

    print(
        "\nTesting immediate repeat..."
    )

    assert guard.canIntervene() is False

    print(
        "Immediate repeat → BLOCKED"
    )

    print("PASS")

    # --------------------------------------------------
    # Wait for cooldown
    # --------------------------------------------------

    print(
        "\nWaiting for cooldown..."
    )

    time.sleep(1.1)

    assert guard.canIntervene() is True

    print(
        "Cooldown completed → ALLOWED"
    )

    print("PASS")

    # --------------------------------------------------
    # Second intervention
    # --------------------------------------------------

    guard.recordIntervention()

    assert guard.interventionCount == 2

    print(
        "\nSecond intervention recorded."
    )

    print("PASS")

    # --------------------------------------------------
    # Maximum intervention limit
    # --------------------------------------------------

    print(
        "\nTesting maximum intervention limit..."
    )

    assert guard.canIntervene() is False

    print(
        "Maximum interventions reached → BLOCKED"
    )

    print("PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    print(
        "\nTesting reset..."
    )

    guard.reset()

    assert guard.interventionCount == 0
    assert guard.canIntervene() is True

    print(
        "Pressure episode reset → ALLOWED"
    )

    print("PASS")

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "\nINTERVENTION GUARD TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()