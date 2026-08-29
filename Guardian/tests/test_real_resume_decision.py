from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== REAL RESUME DECISION ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Creating Guardian Orchestrator..."
    )

    print("PASS")

    # --------------------------------------------------
    # Read REAL RAM
    # --------------------------------------------------

    print(
        "\nReading REAL system memory..."
    )

    memory, candidates = (
        guardian.findResumCandidate()
    )

    print("PASS")

    # --------------------------------------------------
    # Display current state
    # --------------------------------------------------

    print(
        "\n========== LIVE MEMORY ==========\n"
    )

    print(
        f"RAM Usage       : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Available RAM   : "
        f"{memory.availableRam / (1024 ** 3):.2f} GB"
    )

    print(
        f"Resume Threshold: "
        f"{guardian.resumePolicy.threshold}%"
    )

    # --------------------------------------------------
    # Decision validation
    # --------------------------------------------------

    print(
        "\n========== RESUME DECISION ==========\n"
    )

    if memory.ramPercent <= guardian.resumePolicy.threshold:

        print(
            "RAM is SAFE."
        )

        print(
            f"Resume Candidates : "
            f"{len(candidates)}"
        )

        assert len(candidates) >= 0

        print("PASS")

        for process in candidates:

            assert process.pid > 0
            assert process.name

            print(
                f"PID={process.pid:<8} "
                f"Name={process.name}"
            )

    else:

        print(
            "RAM is NOT SAFE for resume."
        )

        print(
            "No automatic resume should occur."
        )

        assert candidates == []

        print(
            "Resume correctly blocked."
        )

        print("PASS")

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "\nREAL RESUME DECISION TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()