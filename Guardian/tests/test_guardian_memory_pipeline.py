from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== Guardian Memory Pipeline ==========\n"
    )

    print("Creating Guardian...")

    guardian = GuardianOrchestrator()

    print("PASS")

    # --------------------------------------------------
    # Collect real RAM
    # --------------------------------------------------

    print("\nCollecting REAL system memory...")

    memory, pressure, decision = (
        guardian.analyzeMemory()
    )

    print("PASS")

    # --------------------------------------------------
    # Display live information
    # --------------------------------------------------

    print(
        "\n========== LIVE MEMORY DECISION ==========\n"
    )

    print(
        f"RAM Usage       : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Total RAM       : "
        f"{memory.totalRam / (1024 ** 3):.2f} GB"
    )

    print(
        f"Used RAM        : "
        f"{memory.usedRam / (1024 ** 3):.2f} GB"
    )

    print(
        f"Available RAM   : "
        f"{memory.availableRam / (1024 ** 3):.2f} GB"
    )

    print(
        f"Swap Usage      : "
        f"{memory.swapPercent:.1f}%"
    )

    print(
        f"Pressure State  : "
        f"{pressure}"
    )

    print(
        f"Description     : "
        f"{pressure.Description}"
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

    print(
        "\nMemory values are valid."
    )

    print("PASS")

    print(
        "\nPressure and decision successfully "
        "calculated from real RAM."
    )

    print("PASS")

    print(
        "\n=========================================="
    )

    print(
        "\nGUARDIAN MEMORY PIPELINE PASSED\n"
    )


if __name__ == "__main__":

    run_test()