
from Guardian.ProcessTracker import ProcessTracker


def run_test():

    print("\n========== Invalid PID Test ==========\n")

    tracker = ProcessTracker()

    invalid_pid = 99999999

    print(f"Testing PID : {invalid_pid}")

    process = tracker.process(invalid_pid)

    print(f"Result      : {process}")

    assert process is None

    print("\nINVALID PID TEST PASSED\n")


if __name__ == "__main__":
    run_test()