import os

from Guardian.ProcessResolver import ProcessResolve
from Guardian.models.ProcessInfo import ProcessInfo


def run_test():

    print("\n========== Process Resolver Test ==========\n")

    resolver = ProcessResolve()

    current_pid = os.getpid()

    print(f"Resolving Current PID : {current_pid}")

    process = resolver.resolve(current_pid)

    assert process is not None
    assert isinstance(process, ProcessInfo)
    assert process.pid == current_pid

    print("PASS")

    print("\n========== Resolved Process ==========\n")

    print(f"PID            : {process.pid}")
    print(f"Name           : {process.name}")
    print(f"User           : {process.userName}")
    print(f"Memory         : {process.memoryMb:.2f} MB")
    print(f"Memory Percent : {process.memoryPercent:.2f}%")
    print(f"Status         : {process.status}")

    print("\nTesting Invalid PID...")

    invalid_process = resolver.resolve(-1)

    assert invalid_process is None

    print("PASS")

    print("\nTesting Non-existing PID...")

    missing_process = resolver.resolve(
        999999999
    )

    assert missing_process is None

    print("PASS")

    print("\n========================================")

    print("\nPROCESS RESOLVER TEST PASSED\n")


if __name__ == "__main__":
    run_test()