from Guardian.ProcessTracker import ProcessTracker
from Guardian.models.ProcessInfo import ProcessInfo


def run_tests():

    print("\n========== Process Tracker Test ==========\n")

    tracker = ProcessTracker()

    print("Reading running processes...")

    processes = tracker.runningProcess()

    assert isinstance(processes, list)

    print(f"Processes Found : {len(processes)}")

    assert len(processes) > 0

    print("\n========== Sample Processes ==========\n")

    for process in processes[:10]:

        print(
            f"PID={process.pid:<7} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    assert all(
        isinstance(process, ProcessInfo)
        for process in processes
    )

    print("\nPROCESS TRACKER TEST PASSED\n")


if __name__ == "__main__":
    run_tests()