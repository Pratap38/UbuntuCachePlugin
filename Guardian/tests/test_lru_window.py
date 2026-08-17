from datetime import datetime, timedelta

from Guardian.LRUManager import LRU
from Guardian.models.WindowInfo import WindowInfo
from Guardian.models.DesktopEnvironment import DesktopEnv


def run_test():

    print("\n========== LRU Window Test ==========\n")

    lru = LRU()

    now = datetime.now()

    old_window = WindowInfo(
        windoId="WINDOW-001",
        pID=1001,
        application="Firefox",
        title="Old Window",
        focused=True,
        timestamp=now - timedelta(minutes=5),
        environment=DesktopEnv.WAYLAND,
    )

    new_window = WindowInfo(
        windoId="WINDOW-002",
        pID=1002,
        application="VS Code",
        title="New Window",
        focused=True,
        timestamp=now,
        environment=DesktopEnv.WAYLAND,
    )

    print("Adding WindowInfo events...")

    lru.updateFromWindow(old_window)
    lru.updateFromWindow(new_window)

    print("PASS")

    print("\nLeast Recently Used:")

    least_recent = lru.leastRecent()

    print(least_recent)

    assert least_recent == [
        1001,
        1002,
    ]

    print("PASS")

    print("\nMost Recently Used:")

    most_recent = lru.mostRecent()

    print(most_recent)

    assert most_recent == [
        1002,
        1001,
    ]

    print("PASS")

    print("\n====================================")

    print("\nLRU WINDOW TEST PASSED\n")


if __name__ == "__main__":
    run_test()