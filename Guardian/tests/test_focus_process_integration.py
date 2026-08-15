import time

from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.models.DesktopEnvironment import DesktopEnv
from Guardian.ProcessTracker import ProcessTracker


def run_test():

    print("\n========== Focus → Process Integration ==========\n")

    print("Creating Wayland Focus Tracker...")

    focus_tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    print("PASS")

    print("\nReading focused window...")

    window = None
    for _ in range(20):
        window = focus_tracker.getActiveWindow()
        if window is not None:
            break
        time.sleep(0.5)

    if window is None:
        focus_tracker.stop()
        raise AssertionError(
            "No focused window payload received after waiting 10 seconds."
        )

    print("PASS")

    print("\n========== Focused Window ==========\n")

    print(f"Application : {window.application}")
    print(f"Title       : {window.title}")
    print(f"PID         : {window.pID}")
    print(f"Window ID   : {window.windoId}")

    assert window.pID is not None
    assert int(window.pID) > 0

    print("\nStarting Process Tracker...")

    process_tracker = ProcessTracker()

    process = process_tracker.process(
        int(window.pID)
    )

    focus_tracker.stop()

    if process is None:
        raise AssertionError(
            f"Focused PID {window.pID} "
            "could not be resolved to a process."
        )

    print("PASS")

    print("\n========== Real Process ==========\n")

    print(f"PID            : {process.pid}")
    print(f"Name           : {process.name}")
    print(f"User           : {process.userName}")
    print(f"Memory         : {process.memoryMb:.2f} MB")
    print(f"Memory Percent  : {process.memoryPercent:.2f}%")
    print(f"Status          : {process.status}")

    assert process.pid == int(window.pID)

    print("\n===================================")

    print("\nFOCUS → PROCESS INTEGRATION PASSED\n")


if __name__ == "__main__":
    run_test()