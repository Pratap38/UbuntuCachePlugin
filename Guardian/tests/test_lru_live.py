import time

from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.models.DesktopEnvironment import DesktopEnv


def run_test():

    print("\n========== Live LRU Test ==========\n")

    print("Creating Wayland Focus Tracker...")

    tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    print("PASS")

    print("\nWaiting for real focus events...")
    print("Switch between Chrome, VS Code and Terminal.")

    seen = {}

    start = time.time()

    while time.time() - start < 20:

        window = tracker.getActiveWindow()

        if window is not None:

            pid = window.pID

            if pid not in seen:

                seen[pid] = window.application

                print(
                    f"\nFOCUS DETECTED"
                    f"\nApplication : {window.application}"
                    f"\nPID         : {window.pID}"
                    f"\nTimestamp   : {window.timestamp}"
                )

        time.sleep(0.5)

    lru = tracker.getLRU()

    tracker.stop()

    print("\n========== LRU History ==========\n")

    for pid in lru.mostRecent():

        print(
            f"PID={pid:<8} "
            f"Application={seen.get(pid, 'Unknown'):<20} "
            f"Last Used={lru.getLastUsed(pid)}"
        )

    assert lru.size() > 0

    print("\n================================")

    print("\nLIVE LRU TEST PASSED\n")


if __name__ == "__main__":
    run_test()