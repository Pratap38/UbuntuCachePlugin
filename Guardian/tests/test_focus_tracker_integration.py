"""
===========================================================

RAM Guardian

Focus Tracker Integration Test

Author : Ubuntu Cache Cleaner Project

===========================================================
"""

from Guardian.DesktopChecker import DesktopChecker
from Guardian.Focus.MockFocusTracker import MockFocusTracker


def run_tests():

    print("\n========== Focus Tracker Integration Test ==========\n")

    print("Starting Desktop Checker...")

    checker = DesktopChecker()

    print("PASS")

    # --------------------------------------------------

    print("Starting Focus Tracker...")

    tracker = MockFocusTracker()

    print("PASS")

    # --------------------------------------------------

    print("Reading Active Window...")

    window = tracker.getActiveWindow()

    print("PASS")

    # --------------------------------------------------

    print("\n========== Desktop ==========\n")

    print(f"Environment        : {checker.current()}")

    print(f"Supports Tracking  : {checker.supportsWindowTracking()}")

    print()

    print("========== Active Window ==========\n")

    print(f"Application        : {window.application}")

    print(f"Title              : {window.title}")

    print(f"PID                : {window.pID}")

    print(f"Window ID          : {window.windoId}")

    print(f"Focused            : {window.focused}")

    print(f"Timestamp          : {window.timestamp}")

    print(f"Environment        : {window.environment}")

    print()

    print("========== Backend Decision ==========\n")

    if checker.isX11():

        print("Backend Selected : FocusTrackerX11")

    elif checker.isWayland():

        print("Backend Selected : FocusTrackerWayland")

    else:

        print("Backend Selected : Unsupported")

    print()

    print("======================================")

    print("\nINTEGRATION TEST PASSED\n")


if __name__ == "__main__":

    run_tests()