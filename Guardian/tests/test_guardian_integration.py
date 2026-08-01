

from Guardian.RAMMonitor import RamMonitor
from Guardian.MemoryPressureDetector import MemoryPressureCheck
from Guardian.GuardianConfig import GuardianConfig


def run_tests():

    print("\n========== Guardian Integration Test ==========\n")

    # --------------------------------------------------

    print("Loading Guardian Configuration...")

    config = GuardianConfig()

    print("PASS")

    # --------------------------------------------------

    print("Starting RAM Monitor...")

    monitor = RamMonitor()

    print("PASS")

    # --------------------------------------------------

    print("Collecting Current Memory Information...")

    memory = monitor.collect()

    print("PASS")

    # --------------------------------------------------

    print("Analyzing Memory Pressure...")

    detector = MemoryPressureCheck()

    state = detector.analyze(memory)

    print("PASS")

    # --------------------------------------------------

    print("\n========== Live System Report ==========\n")

    print(f"Timestamp          : {memory.timestamp}")

    print(f"Total RAM          : {memory.totalRamGb:.2f} GB")

    print(f"Used RAM           : {memory.usedRamGb:.2f} GB")

    print(f"Available RAM      : {memory.availableRamGb:.2f} GB")

    print(f"RAM Usage          : {memory.ramPercent:.1f}%")

    print()

    print(f"Total Swap         : {memory.totalSwapGb:.2f} GB")

    print(f"Used Swap          : {memory.usedSwapGb:.2f} GB")

    print(f"Swap Usage         : {memory.swapPercent:.1f}%")

    print()

    print(f"Pressure State     : {state}")

    print(f"Description        : {state.Description}")

    print(f"Color              : {state.color}")

    print(f"Icon               : {state.icon}")

    print()

    print("========== Current Thresholds ==========\n")

    print(
        f"Warning Threshold  : "
        f"{config.get('warningThreshold')}%"
    )

    print(
        f"Critical Threshold : "
        f"{config.get('criticalThreshold')}%"
    )

    print(
        f"Emergency Threshold: "
        f"{config.get('emergencyThreshold')}%"
    )

    print("\n========================================")

    print("\nINTEGRATION TEST PASSED\n")


if __name__ == "__main__":

    run_tests()
