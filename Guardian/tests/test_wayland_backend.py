"""
===========================================================

RAM Guardian

Wayland Backend Test

Author : Ubuntu Cache Cleaner Project

===========================================================
"""

from Guardian.platform.Wayland.DBusClient import DbusClient
from Guardian.platform.Wayland.WaylandBackend import WaylandBackend
from Guardian.platform.Wayland.WindowDetector import WindowDetector
from Guardian.platform.Wayland.ApplicationResolver import ApplicationPauseContinue


def run_tests():

    print("\n========== Wayland Backend Test ==========\n")

    # --------------------------------------------------

    print("Testing DBus Client...")

    client = DbusClient()

    assert client is not None

    print("PASS")

    # --------------------------------------------------

    print("Testing Wayland Backend...")

    backend = WaylandBackend()

    assert backend.isAvail()

    print("PASS")

    # --------------------------------------------------

    print("Testing Window Detector...")

    detector = WindowDetector()

    assert detector.isAvail()

    print("PASS")

    # --------------------------------------------------

    print("Testing Detection Support...")

    assert detector.supportDetector()

    print("PASS")

    # --------------------------------------------------

    print("Testing Application Resolver...")

    resolver = ApplicationPauseContinue()

    assert resolver is not None

    print("PASS")

    # --------------------------------------------------

    print("\n========== Backend Report ==========\n")

    print(f"Backend Available      : {backend.isAvail()}")

    print(f"GNOME Version          : {backend.getShellVersion()}")

    print(f"Detection Supported    : {detector.supportDetector()}")

    print()

    print("====================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()