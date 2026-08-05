"""
===========================================================

RAM Guardian

Desktop Integration Test

Author : Ubuntu Cache Cleaner Project

===========================================================
"""

from Guardian.DesktopChecker import DesktopChecker
from Guardian.models.DesktopEnvironment import DesktopEnv


def run_tests():

    print("\n========== Desktop Integration Test ==========\n")

    print("Starting Desktop Checker...")

    checker = DesktopChecker()

    print("PASS")

    # ----------------------------------------------------

    print("Detecting Desktop Environment...")

    environment = checker.current()

    print("PASS")

    # ----------------------------------------------------

    print("\n========== Desktop Report ==========\n")

    print(f"Environment          : {environment}")

    print(f"Description          : {environment.Description}")

    print(f"Supports Tracking    : {checker.supportsWindowTracking()}")

    print()

    if checker.isX11():

        print("Selected Backend     : FocusTrackerX11")

    elif checker.isWayland():

        print("Selected Backend     : FocusTrackerWayland")

    else:

        print("Selected Backend     : None")

    print()

    print("========== Startup Decision ==========\n")

    if checker.supportsWindowTracking():

        print("Window Tracking : ENABLED")

    else:

        print("Window Tracking : LIMITED")

        print(
            "Guardian will use the "
            "Wayland-compatible backend."
        )

    print("\n======================================")

    print("\nINTEGRATION TEST PASSED\n")


if __name__ == "__main__":

    run_tests()