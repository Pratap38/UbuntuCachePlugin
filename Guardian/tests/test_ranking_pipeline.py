from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== Ranking Pipeline ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Creating Guardian Orchestrator..."
    )

    print("PASS")

    # --------------------------------------------------
    # Read real candidates
    # --------------------------------------------------

    print(
        "\nReading real system candidates..."
    )

    memory, pressure, decision, ranked = (
        guardian.rankCandidate()
    )

    print("PASS")

    # --------------------------------------------------
    # Display memory state
    # --------------------------------------------------

    print(
        "\n========== LIVE MEMORY ==========\n"
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
    # Warning / Normal path
    # --------------------------------------------------

    if not decision:

        print(
            "\nNo action required."
        )

        print(
            "Ranking skipped."
        )

        print("PASS")

        print(
            "\n===================================="
        )

        print(
            "\nRANKING PIPELINE PASSED\n"
        )

        return

    # --------------------------------------------------
    # Critical path
    # --------------------------------------------------

    print(
        "\nAction required."
    )

    print(
        f"Ranked Candidates : "
        f"{len(ranked)}"
    )

    assert len(ranked) > 0

    print("PASS")

    # --------------------------------------------------
    # Validate descending RAM order
    # --------------------------------------------------

    print(
        "\nValidating RAM ranking..."
    )

    for index in range(
        len(ranked) - 1
    ):

        current = ranked[index]
        nextProcess = ranked[index + 1]

        assert (
            current.memoryBytes
            >=
            nextProcess.memoryBytes
        )

    print(
        "RAM ranking is correctly "
        "descending."
    )

    print("PASS")

    # --------------------------------------------------
    # Top 10
    # --------------------------------------------------

    topProcesses = ranked[:10]

    print(
        "\n========== Top RAM Consumers ==========\n"
    )

    for process in topProcesses:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    assert len(topProcesses) <= 10

    print(
        "\nTop 10 selection verified."
    )

    print("PASS")

    print(
        "\n========================================"
    )

    print(
        "\nRANKING PIPELINE PASSED\n"
    )


if __name__ == "__main__":

    run_test()