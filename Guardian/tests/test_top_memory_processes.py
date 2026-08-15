from Guardian.ProcessTracker import ProcessTracker


def run_test():

    print("\n========== Top Memory Processes Test ==========\n")

    tracker = ProcessTracker()

    processes = tracker.topMemoryProcesses(10)

    print(f"Processes Returned : {len(processes)}")

    assert isinstance(processes, list)
    assert len(processes) <= 10

    # Verify descending RAM order
    for previous, current in zip(
        processes,
        processes[1:]
    ):
        assert previous.memoryBytes >= current.memoryBytes

    print("\n========== Top RAM Consumers ==========\n")

    for process in processes:

        print(
            f"PID={process.pid:<7} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    print("\n========================================")

    print("\nTOP MEMORY PROCESS TEST PASSED\n")


if __name__ == "__main__":
    run_test()