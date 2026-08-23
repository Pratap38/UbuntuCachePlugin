from Guardian.NotificationManager import NotificationManager
from Guardian.models.PressureState import PressureState


class TestNotificationManager(
    NotificationManager
):

    def __init__(self):

        super().__init__()

        self.sentNotifications = []

    def send(
        self,
        title: str,
        message: str,
        urgency: str = "normal"
    ) -> bool:

        self.sentNotifications.append(
            (
                title,
                message,
                urgency
            )
        )

        return True


def run_test():

    print(
        "\n========== Notification State Test ==========\n"
    )

    manager = TestNotificationManager()

    # --------------------------------------------------
    # Early warning
    # --------------------------------------------------

    print("Testing early warning...")

    assert manager.earlyWarning(85.0) is True

    assert manager.earlyWarning(86.0) is False
    assert manager.earlyWarning(87.0) is False

    print(
        "85% → SEND"
    )

    print(
        "86% → NO REPEAT"
    )

    print(
        "87% → NO REPEAT"
    )

    print("PASS")

    # --------------------------------------------------
    # Critical
    # --------------------------------------------------

    print("\nTesting critical notification...")

    assert manager.notify(
        PressureState.CRITICAL,
        90.2
    ) is True

    assert manager.notify(
        PressureState.CRITICAL,
        91.5
    ) is False

    print(
        "90.2% → SEND"
    )

    print(
        "91.5% → NO REPEAT"
    )

    print("PASS")

    # --------------------------------------------------
    # Emergency
    # --------------------------------------------------

    print("\nTesting emergency notification...")

    assert manager.notify(
        PressureState.EMERGENCY,
        97.1
    ) is True

    assert manager.notify(
        PressureState.EMERGENCY,
        98.0
    ) is False

    print(
        "97.1% → SEND"
    )

    print(
        "98.0% → NO REPEAT"
    )

    print("PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    print("\nTesting notification reset...")

    manager.notify(
        PressureState.NORMAL,
        70.0
    )

    assert manager.earlyWarningSent is False
    assert manager.warningSent is False
    assert manager.criticalSent is False
    assert manager.emergencySent is False

    print(
        "NORMAL state → notification state reset"
    )

    print("PASS")

    # --------------------------------------------------

    print("\n==============================================")

    print(
        "\nNOTIFICATION STATE TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()