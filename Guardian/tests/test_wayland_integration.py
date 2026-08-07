"""
===========================================================

RAM Guardian

Wayland Integration Test

Author : Ubuntu Cache Cleaner Project

===========================================================
"""

from Guardian.Focus.FocusTrackerWayland import FocusTrackerWayland


def run_tests():

    print("\n========== Wayland Integration Test ==========\n")

    print("Starting Focus Tracker...")

    tracker = FocusTrackerWayland()

    print("PASS")

    # --------------------------------------------------

    print("Checking Backend Support...")

    assert tracker.isSupported()

    print("PASS")

    # --------------------------------------------------

    print("Reading Active Window...")

    window = tracker.getActiveWindow()

    if window is None:

        print("No active window detected.")

    else:

        print("PASS")

        print()

        print("========== Window Information ==========\n")

        print(f"Application : {window.application}")

        print(f"Title       : {window.title}")

        print(f"PID         : {window.pid}")

        print(f"Window ID   : {window.window_id}")

        print(f"Environment : {window.environment}")

        print(f"Focused     : {window.focused}")

        print(f"Timestamp   : {window.timestamp}")

    print()

    print("========================================")

    print("\nINTEGRATION TEST PASSED\n")


if __name__ == "__main__":

    run_tests()