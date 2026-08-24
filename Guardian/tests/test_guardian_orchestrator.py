from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== Guardian Orchestrator Test ==========\n"
    )

    print("Creating Guardian Orchestrator...")

    guardian = GuardianOrchestrator()

    print("PASS")

    # --------------------------------------------------
    # Verify core components
    # --------------------------------------------------

    print("\nChecking core components...")

    assert guardian.ramMonitor is not None
    assert guardian.pressureCheck is not None
    assert guardian.decisionEngine is not None

    print("Monitoring + Decision components → PASS")

    # --------------------------------------------------
    # Verify process components
    # --------------------------------------------------

    print("\nChecking process components...")

    assert guardian.candidateSelector is not None
    assert guardian.memoryRanker is not None
    assert guardian.pauseManager is not None
    assert guardian.resumeManager is not None

    print("Process components → PASS")

    # --------------------------------------------------
    # Verify state components
    # --------------------------------------------------

    print("\nChecking state components...")

    assert guardian.pauseRegistry is not None
    assert guardian.resumePolicy is not None

    print("State components → PASS")

    # --------------------------------------------------
    # Verify support components
    # --------------------------------------------------

    print("\nChecking support components...")

    assert guardian.eventHistory is not None
    assert guardian.notificationManager is not None

    print("History + Notification → PASS")

    # --------------------------------------------------

    print("\n==============================================")

    print(
        "\nGUARDIAN ORCHESTRATOR TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()