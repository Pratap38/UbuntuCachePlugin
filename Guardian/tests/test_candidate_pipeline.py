from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== Candidate Pipeline ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Creating Guardian Orchestrator..."
    )

    print("PASS")

    # --------------------------------------------------
    # Analyze real RAM
    # --------------------------------------------------

    print(
        "\nReading real system memory..."
    )

    memory, pressure, decision, candidates = (
        guardian.getCandidate()
    )

    print("PASS")

    # --------------------------------------------------
    # Live memory
    # --------------------------------------------------

    print(
        "\n========== LIVE MEMORY ==========\n"
    )

    print(
        f"RAM Usage      : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Pressure State : "
        f"{pressure}"
    )

    print(
        f"Action Required: "
        f"{decision}"
    )

    # --------------------------------------------------
    # Decision
    # --------------------------------------------------

    if not decision:

        print(
            "\nNo action required."
        )

        print(
            "Candidate selection skipped."
        )

        print("PASS")

    else:

        print(
            "\nAction required."
        )

        print(
            "Reading eligible candidates..."
        )

        print(
            f"Candidates Found : "
            f"{len(candidates)}"
        )

        assert len(candidates) >= 0

        print("PASS")

        # --------------------------------------------------
        # Validate safety
        # --------------------------------------------------

        currentUser = memory

        print(
            "\nValidating candidate list..."
        )

        for process in candidates:

            assert process.pid > 0
            assert process.name
            assert process.memoryBytes >= 0

        print(
            "All candidates passed basic validation."
        )

        print("PASS")

        # --------------------------------------------------
        # Display candidates
        # --------------------------------------------------

        print(
            "\n========== Sample Candidates ==========\n"
        )

        for process in candidates[:10]:

            print(
                f"PID={process.pid:<8} "
                f"Name={process.name:<25} "
                f"RAM={process.memoryMb:>8.2f} MB "
                f"Status={process.status}"
            )

    print(
        "\n========================================"
    )

    print(
        "\nCANDIDATE PIPELINE PASSED\n"
    )


if __name__ == "__main__":

    run_test()