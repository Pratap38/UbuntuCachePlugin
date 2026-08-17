import time

from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.models.DesktopEnvironment import DesktopEnv
from Guardian.ProcessResolver import ProcessResolve


def run_test():

    print("\n========== Focus → Process Resolver ==========\n")

    # --------------------------------------------------
    # 1. Start Focus Tracker
    # --------------------------------------------------

    print("Creating Wayland Focus Tracker...")

    focus_tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    print(
        f"Tracker : "
        f"{type(focus_tracker).__name__}"
    )

    print("PASS")

    # --------------------------------------------------
    # 2. Wait for real focus payload
    # --------------------------------------------------

    print("\nWaiting for real focused application...")

    window = None

    for _ in range(20):

        window = focus_tracker.getActiveWindow()

        if window is not None:
            break

        time.sleep(0.5)

    if window is None:

        focus_tracker.stop()

        raise AssertionError(
            "No real focused window received."
        )

    print("PASS")

    # --------------------------------------------------
    # 3. Display focused window
    # --------------------------------------------------

    print("\n========== Focused Window ==========\n")

    print(
        f"Application : "
        f"{window.application}"
    )

    print(
        f"Title       : "
        f"{window.title}"
    )

    print(
        f"PID         : "
        f"{window.pID}"
    )

    print(
        f"Window ID   : "
        f"{window.windoId}"
    )

    print(
        f"Environment : "
        f"{window.environment}"
    )

    assert window.pID > 0

    # --------------------------------------------------
    # 4. Resolve PID
    # --------------------------------------------------

    print("\nResolving focused PID...")

    resolver = ProcessResolve()

    process = resolver.resolve(
        window.pID
    )

    assert process is not None

    print("PASS")

    # --------------------------------------------------
    # 5. Verify resolved process
    # --------------------------------------------------

    print("\n========== Resolved Process ==========\n")

    print(
        f"PID            : "
        f"{process.pid}"
    )

    print(
        f"Name           : "
        f"{process.name}"
    )

    print(
        f"User           : "
        f"{process.userName}"
    )

    print(
        f"Memory         : "
        f"{process.memoryMb:.2f} MB"
    )

    print(
        f"Memory Percent : "
        f"{process.memoryPercent:.2f}%"
    )

    print(
        f"Status         : "
        f"{process.status}"
    )

    # --------------------------------------------------
    # 6. Verify PID consistency
    # --------------------------------------------------

    assert process.pid == window.pID

    print("\nPID Consistency : PASS")

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    focus_tracker.stop()

    print("\n========================================")

    print(
        "\nFOCUS → PROCESS RESOLVER "
        "INTEGRATION PASSED\n"
    )


if __name__ == "__main__":
    run_test()