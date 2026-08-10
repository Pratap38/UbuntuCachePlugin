import time

from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.models.DesktopEnvironment import DesktopEnv


def run_test():

    print("\n========== Factory → Wayland Live Test ==========\n")

    print("Creating tracker through Factory...")

    tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    print(f"Tracker : {type(tracker).__name__}")

    assert type(tracker).__name__ == "FocusTrackerWayland"

    print("PASS")

    print("\nWaiting for real GNOME focus payload...")

    for _ in range(20):

        window = tracker.getActiveWindow()

        if window is not None:

            print("\n========== REAL FOCUS ==========\n")

            print(f"Application : {window.application}")
            print(f"Title       : {window.title}")
            print(f"PID         : {window.pID}")
            print(f"Window ID   : {window.windoId}")
            print(f"Focused     : {window.focused}")
            print(f"Environment : {window.environment}")
            print(f"Timestamp   : {window.timestamp}")

            print("\n================================")

            print("\nFACTORY → WAYLAND LIVE TEST PASSED\n")

            tracker.stop()

            return

        time.sleep(0.5)

    tracker.stop()

    raise AssertionError(
        "No real GNOME focus payload received."
    )


if __name__ == "__main__":
    run_test()