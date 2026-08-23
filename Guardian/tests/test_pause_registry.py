from datetime import datetime

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print("\n========== Pause Registry Test ==========\n")

    registry = PauseRegistry()

    # --------------------------------------------------
    # Create paused process record
    # --------------------------------------------------

    print("Creating paused process record...")

    process = PauseProcess(
        pid=1001,
        name="chrome",
        pausedAt=datetime.now(),
        reason="RAM Critical"
    )

    print("PASS")

    # --------------------------------------------------
    # Add
    # --------------------------------------------------

    print("\nAdding process to registry...")

    assert registry.add(process) is True

    print("Process registered.")
    print("PASS")

    # --------------------------------------------------
    # Contains
    # --------------------------------------------------

    print("\nChecking registry ownership...")

    assert registry.contains(1001)

    print("PID=1001 → REGISTERED")
    print("PASS")

    # --------------------------------------------------
    # Get
    # --------------------------------------------------

    print("\nReading process record...")

    saved = registry.get(1001)

    assert saved is not None
    assert saved.pid == 1001
    assert saved.name == "chrome"
    assert saved.reason == "RAM Critical"

    print(
        f"PID    : {saved.pid}"
    )

    print(
        f"Name   : {saved.name}"
    )

    print(
        f"Reason : {saved.reason}"
    )

    print("PASS")

    # --------------------------------------------------
    # Duplicate
    # --------------------------------------------------

    print("\nTesting duplicate registration...")

    assert registry.add(process) is False

    print("Duplicate → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    print("\nChecking registry count...")

    assert registry.count() == 1

    print(
        f"Registered Processes : {registry.count()}"
    )

    print("PASS")

    # --------------------------------------------------
    # Remove
    # --------------------------------------------------

    print("\nRemoving process...")

    assert registry.remove(1001) is True

    assert registry.contains(1001) is False

    print("Process removed.")
    print("PASS")

    # --------------------------------------------------
    # Empty check
    # --------------------------------------------------

    print("\nChecking final registry...")

    assert registry.count() == 0

    print("Registry is empty.")
    print("PASS")

    print("\n========================================")

    print("\nPAUSE REGISTRY TEST PASSED\n")


if __name__ == "__main__":

    run_test()