from Guardian.GuardianEngine import GuardianEngine


def run_test():

    print(
        "\n========== Guardian Notification Loop ==========\n"
    )

    engine = GuardianEngine(
        interval=1.0
    )

    print(
        "Creating Guardian Engine..."
    )

    print("PASS")

    # --------------------------------------------------
    # First REAL cycle
    # --------------------------------------------------

    print(
        "\nRunning REAL monitoring cycle..."
    )

    result = engine.runCycle()

    print("PASS")

    memory = result["memory"]
    pressure = result["pressure"]
    decision = result["decision"]
    notificationSent = result["notificationSent"]

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    print(
        "\n========== LIVE GUARDIAN ==========\n"
    )

    print(
        f"RAM Usage       : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Pressure State  : "
        f"{pressure}"
    )

    print(
        f"Action Required : "
        f"{decision}"
    )

    print(
        f"Notification    : "
        f"{notificationSent}"
    )

    # --------------------------------------------------
    # Validate live data
    # --------------------------------------------------

    assert 0 <= memory.ramPercent <= 100

    assert pressure is not None

    assert isinstance(
        decision,
        bool
    )

    assert isinstance(
        notificationSent,
        bool
    )

    print(
        "\nLive notification decision validated."
    )

    print("PASS")

    # --------------------------------------------------
    # Second cycle
    # --------------------------------------------------

    print(
        "\nRunning second monitoring cycle..."
    )

    secondResult = engine.runCycle()

    print("PASS")

    secondNotification = (
        secondResult["notificationSent"]
    )

    print(
        f"Second Notification : "
        f"{secondNotification}"
    )

    # --------------------------------------------------
    # Anti-spam validation
    # --------------------------------------------------

    print(
        "\nChecking notification anti-spam..."
    )

    if (
        pressure == secondResult["pressure"]
    ):

        assert secondNotification is False

        print(
            "Same pressure state → "
            "notification suppressed."
        )

        print("PASS")

    else:

        print(
            "Pressure state changed → "
            "new notification decision allowed."
        )

        print("PASS")

    # --------------------------------------------------
    # Stop
    # --------------------------------------------------

    engine.stop()

    assert engine.running is False

    print(
        "\nGuardian stopped cleanly."
    )

    print("PASS")

    print(
        "\n=============================================="
    )

    print(
        "\nGUARDIAN NOTIFICATION LOOP TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()