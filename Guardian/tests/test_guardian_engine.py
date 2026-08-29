from Guardian.GuardianEngine import GuardianEngine


def run_test():

    print(
        "\n========== Guardian Engine Test ==========\n"
    )

    print(
        "Creating Guardian Engine..."
    )

    engine = GuardianEngine(
        interval=1.0
    )

    print("PASS")

    # --------------------------------------------------
    # Initial state
    # --------------------------------------------------

    print(
        "\nChecking initial state..."
    )

    assert engine.running is False

    print(
        "Guardian is STOPPED."
    )

    print("PASS")

    # --------------------------------------------------
    # Run one REAL cycle
    # --------------------------------------------------

    print(
        "\nRunning one REAL monitoring cycle..."
    )

    result = engine.runCycle()

    print("PASS")

    memory = result["memory"]
    pressure = result["pressure"]
    decision = result["decision"]

    # --------------------------------------------------
    # Live data
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

    # --------------------------------------------------
    # Validate
    # --------------------------------------------------

    assert 0 <= memory.ramPercent <= 100

    assert 0 <= memory.swapPercent <= 100

    assert pressure is not None

    assert isinstance(
        decision,
        bool
    )

    print(
        "\nReal memory cycle validated."
    )

    print("PASS")

    # --------------------------------------------------
    # Stop test
    # --------------------------------------------------

    engine.stop()

    assert engine.running is False

    print(
        "\nGuardian stopped cleanly."
    )

    print("PASS")

    print(
        "\n=========================================="
    )

    print(
        "\nGUARDIAN ENGINE TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()