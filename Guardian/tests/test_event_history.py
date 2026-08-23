from datetime import datetime

from Guardian.EventHistory import EventHistory
from Guardian.models.GuardianEvent import GuardianEvent


def run_test():

    print(
        "\n========== Event History Test ==========\n"
    )

    history = EventHistory()

    # --------------------------------------------------
    # Create PAUSED event
    # --------------------------------------------------

    print("Creating PAUSED event...")

    paused = GuardianEvent(
        eventType="PAUSED",
        pid=1001,
        processName="chrome",
        timestamp=datetime.now(),
        reason="RAM Critical",
        ramPercent=90.4
    )

    print("PASS")

    # --------------------------------------------------
    # Add event
    # --------------------------------------------------

    print("\nAdding PAUSED event...")

    assert history.add(paused)

    print("Event added.")
    print("PASS")

    # --------------------------------------------------
    # Create RESUMED event
    # --------------------------------------------------

    print("\nCreating RESUMED event...")

    resumed = GuardianEvent(
        eventType="RESUMED",
        pid=1001,
        processName="chrome",
        timestamp=datetime.now(),
        reason="RAM Normal",
        ramPercent=72.3
    )

    assert history.add(resumed)

    print("Event added.")
    print("PASS")

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    print("\nChecking event count...")

    assert history.count() == 2

    print(
        f"Events Stored : {history.count()}"
    )

    print("PASS")

    # --------------------------------------------------
    # Latest
    # --------------------------------------------------

    print("\nChecking latest event...")

    latest = history.latest()

    assert latest is not None
    assert latest.eventType == "RESUMED"
    assert latest.pid == 1001

    print(
        f"Latest Event : {latest.eventType}"
    )

    print("PASS")

    # --------------------------------------------------
    # Process history
    # --------------------------------------------------

    print("\nChecking process history...")

    processEvents = history.forProcess(1001)

    assert len(processEvents) == 2

    print(
        f"Events for PID 1001 : "
        f"{len(processEvents)}"
    )

    print("PASS")

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    print("\n========== Stored Events ==========\n")

    for event in history.getAll():

        print(event)

    # --------------------------------------------------

    print("\n===================================")

    print(
        "\nEVENT HISTORY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()