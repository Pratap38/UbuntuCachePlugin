from Guardian.NotificationManager import NotificationManager
from Guardian.models.PressureState import PressureState


def run_test():

    print("\n========== Notification Manager Test ==========\n")

    manager = NotificationManager()

    # --------------------------------------------------
    # Early warning
    # --------------------------------------------------

    print("Testing early warning notification...")

    result = manager.earlyWarning(
        ramPercent=85.5
    )

    assert result is True

    print("Early warning sent.")
    print("PASS")

    # --------------------------------------------------
    # Warning
    # --------------------------------------------------

    print("\nTesting WARNING notification...")

    result = manager.notify(
        PressureState.WARNING,
        82.0
    )

    assert result is True

    print("Warning notification sent.")
    print("PASS")

    # --------------------------------------------------
    # Critical
    # --------------------------------------------------

    print("\nTesting CRITICAL notification...")

    result = manager.notify(
        PressureState.CRITICAL,
        90.8
    )

    assert result is True

    print("Critical notification sent.")
    print("PASS")

    # --------------------------------------------------
    # Emergency
    # --------------------------------------------------

    print("\nTesting EMERGENCY notification...")

    result = manager.notify(
        PressureState.EMERGENCY,
        97.5
    )

    assert result is True

    print("Emergency notification sent.")
    print("PASS")

    # --------------------------------------------------

    print("\n===============================================")

    print("\nNOTIFICATION MANAGER TEST PASSED\n")


if __name__ == "__main__":

    run_test()