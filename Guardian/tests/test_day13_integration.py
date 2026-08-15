import time

from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.models.DesktopEnvironment import DesktopEnv
from Guardian.ProcessTracker import ProcessTracker
from Guardian.GuardianConfig import GuardianConfig


def run_test():

    print("\n========== RAM Guardian Day 13 Integration ==========\n")

    # --------------------------------------------------
    # 1. Create Focus Tracker
    # --------------------------------------------------

    print("Starting Focus Tracker...")

    focus_tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    print(f"Tracker : {type(focus_tracker).__name__}")
    print("PASS")

    # --------------------------------------------------
    # 2. Wait for real GNOME focus payload
    # --------------------------------------------------

    print("\nWaiting for focused application...")

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
    # 3. Display focused application
    # --------------------------------------------------

    print("\n========== Focused Application ==========\n")

    print(f"Application : {window.application}")
    print(f"Title       : {window.title}")
    print(f"PID         : {window.pID}")
    print(f"Window ID   : {window.windoId}")
    print(f"Environment : {window.environment}")

    assert window.pID is not None
    assert int(window.pID) > 0

    # --------------------------------------------------
    # 4. Resolve focused PID
    # --------------------------------------------------

    print("\nResolving focused PID...")

    tracker = ProcessTracker()

    focused_process = tracker.process(
        int(window.pID)
    )

    assert focused_process is not None

    print("PASS")

    print("\n========== Focused Process ==========\n")

    print(f"PID            : {focused_process.pid}")
    print(f"Name           : {focused_process.name}")
    print(f"User           : {focused_process.userName}")
    print(f"Memory         : {focused_process.memoryMb:.2f} MB")
    print(f"Memory Percent : {focused_process.memoryPercent:.2f}%")
    print(f"Status         : {focused_process.status}")

    assert focused_process.pid == int(window.pID)

    # --------------------------------------------------
    # 5. User process filtering
    # --------------------------------------------------

    print("\nFiltering user processes...")

    user_processes = tracker.userProcess()

    assert isinstance(
        user_processes,
        list
    )

    print(
        f"User Processes : "
        f"{len(user_processes)}"
    )

    print("PASS")

    # --------------------------------------------------
    # 6. Verify whitelist
    # --------------------------------------------------

    config = GuardianConfig()

    whitelist = config.get(
        "whitelist",
        []
    )

    for process in user_processes:

        assert process.name not in whitelist

    print("Whitelist Protection : PASS")

    # --------------------------------------------------
    # 7. Top RAM processes
    # --------------------------------------------------

    print("\nFinding top RAM consumers...")

    top_processes = tracker.topMemoryProcesses(
        10
    )

    assert len(top_processes) <= 10

    for previous, current in zip(
        top_processes,
        top_processes[1:]
    ):

        assert (
            previous.memoryBytes
            >= current.memoryBytes
        )

    print("PASS")

    print("\n========== Top RAM Consumers ==========\n")

    for process in top_processes:

        print(
            f"PID={process.pid:<7} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    focus_tracker.stop()

    print("\n==============================================")

    print("\nDAY 13 INTEGRATION TEST PASSED")

    print("\nProcess discovery       : PASS")
    print("PID resolution          : PASS")
    print("Focus → Process         : PASS")
    print("User filtering          : PASS")
    print("Whitelist protection   : PASS")
    print("RAM sorting             : PASS")

    print("\n========== DAY 13 COMPLETE ==========\n")


if __name__ == "__main__":

    run_test()