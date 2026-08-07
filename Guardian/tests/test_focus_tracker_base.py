from Guardian.Focus.MockFocusTracker import MockFocusTracker
from Guardian.models.WindowInfo import WindowInfo


def run_tests():

    print("\n========== Focus Tracker Test ==========\n")

    tracker = MockFocusTracker()

    # -----------------------------------------------------

    print("Testing Tracker Object...")

    assert isinstance(

        tracker,

        MockFocusTracker

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing Active Window...")

    window = tracker.getActiveWindow()

    assert isinstance(

        window,

        WindowInfo

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing Focused Application...")

    app = tracker.getFocusedApplication()

    assert app == "Firefox"

    print("PASS")

    # -----------------------------------------------------

    print("Testing Support Check...")

    assert tracker.isSupported()

    print("PASS")

    # -----------------------------------------------------

    print("Testing Refresh...")

    oldTime = window.timestamp

    tracker.refresh()

    newTime = tracker.getActiveWindow().timestamp

    assert newTime >= oldTime

    print("PASS")

    # -----------------------------------------------------

    print("Testing Window Change...")

    tracker.setWindow(

        application="VS Code",

        title="main.py",

        pid=5555

    )

    window = tracker.getActiveWindow()

    assert window.application == "VS Code"

    assert window.title == "main.py"

    assert window.pID == 5555

    print("PASS")

    # -----------------------------------------------------

    print("\n========== Current Window ==========\n")

    print(f"Application : {window.application}")

    print(f"Title       : {window.title}")

    print(f"PID         : {window.pID}")

    print(f"Window ID   : {window.windoId}")

    print(f"Focused     : {window.focused}")

    print(f"Environment : {window.environment}")

    print()

    print("====================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()