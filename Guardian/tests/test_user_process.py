from Guardian.ProcessTracker import ProcessTracker
from Guardian.GuardianConfig import GuardianConfig


def run_test():

    print("\n========== User Process Test ==========\n")

    tracker = ProcessTracker()
    config = GuardianConfig()

    processes = tracker.userProcess()

    print(f"User Processes Found : {len(processes)}")

    assert isinstance(processes, list)
    assert len(processes) > 0

    currentUser = processes[0].userName

    print(f"User                  : {currentUser}")

    whitelist = config.get(
        "whitelist",
        []
    )

    print("\n========== Sample User Processes ==========\n")

    for process in processes[:15]:

        print(
            f"PID={process.pid:<7} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

        assert process.userName == currentUser
        assert process.name not in whitelist

    print("\n============================================")

    print("\nUSER PROCESS TEST PASSED\n")


if __name__ == "__main__":
    run_test()