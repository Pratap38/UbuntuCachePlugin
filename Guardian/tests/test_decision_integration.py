from Guardian.RAMMonitor import RamMonitor
from Guardian.MemoryPressureDetector import MemoryPressureCheck
from Guardian.DecisionEngine import DecisionEngine


def run_test():

    print("\n========== Decision Engine Integration ==========\n")

    # --------------------------------------------------
    # 1. Start RAM Monitor
    # --------------------------------------------------

    print("Starting RAM Monitor...")

    monitor = RamMonitor()

    print("PASS")

    # --------------------------------------------------
    # 2. Collect REAL memory information
    # --------------------------------------------------

    print("\nCollecting real system memory...")

    memory = monitor.collect()

    print("PASS")

    # --------------------------------------------------
    # 3. Analyze REAL memory pressure
    # --------------------------------------------------

    print("\nAnalyzing memory pressure...")

    pressureChecker = MemoryPressureCheck()

    state = pressureChecker.analyze(
        memory
    )

    print("PASS")

    # --------------------------------------------------
    # 4. Make decision
    # --------------------------------------------------

    print("\nRunning Decision Engine...")

    engine = DecisionEngine()

    actionRequired = engine.decide(
        state
    )

    print("PASS")

    # --------------------------------------------------
    # 5. Display REAL system information
    # --------------------------------------------------

    print("\n========== LIVE MEMORY DECISION ==========\n")

    print(
        f"RAM Usage       : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Total RAM       : "
        f"{memory.totalRamGb:.2f} GB"
    )

    print(
        f"Used RAM        : "
        f"{memory.usedRamGb:.2f} GB"
    )

    print(
        f"Available RAM   : "
        f"{memory.availableRamGb:.2f} GB"
    )

    print(
        f"Swap Usage      : "
        f"{memory.swapPercent:.1f}%"
    )

    print(
        f"Pressure State  : "
        f"{state}"
    )

    print(
        f"Description     : "
        f"{state.Description}"
    )

    print(
        f"Action Required : "
        f"{actionRequired}"
    )

    print()

    # --------------------------------------------------
    # 6. Verify decision consistency
    # --------------------------------------------------

    assert actionRequired == state.RequireAction()

    print(
        "Decision matches pressure state."
    )

    print("PASS")

    print("\n============================================")

    print(
        "\nDECISION ENGINE INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()