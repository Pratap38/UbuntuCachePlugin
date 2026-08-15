import os

from Guardian.ProcessTracker import ProcessTracker
from Guardian.models.ProcessInfo import ProcessInfo


def run_test():

    print("\n========== Process PID Test ==========\n")

    tracker = ProcessTracker()

    current_pid = os.getpid()

    print(f"Testing PID : {current_pid}")

    process = tracker.process(current_pid)

    assert process is not None

    assert isinstance(
        process,
        ProcessInfo
    )

    assert process.pid == current_pid

    print("\n========== Process Information ==========\n")

    print(f"PID            : {process.pid}")
    print(f"Name           : {process.name}")
    print(f"User           : {process.userName}")
    print(f"Memory         : {process.memoryMb:.2f} MB")
    print(f"Memory Percent  : {process.memoryPercent:.2f}%")
    print(f"Status          : {process.status}")

    print("\n========================================")

    print("\nPROCESS PID TEST PASSED\n")


if __name__ == "__main__":
    run_test()