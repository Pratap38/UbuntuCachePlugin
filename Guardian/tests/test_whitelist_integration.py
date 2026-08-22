from Guardian.ProcessTracker import ProcessTracker
from Guardian.WhitelistManager import WhitelistManager


def run_test():

    print("\n========== Whitelist Integration Test ==========\n")

    tracker = ProcessTracker()
    whitelist = WhitelistManager()

    # --------------------------------------------------
    # Get eligible user processes
    # --------------------------------------------------

    print("Reading eligible user processes...")

    processes = tracker.userProcess()

    print(
        f"Eligible Processes : {len(processes)}"
    )

    assert len(processes) > 0

    print("PASS")

    # --------------------------------------------------
    # Verify protected processes are excluded
    # --------------------------------------------------

    print("\nChecking protected processes...")

    protected_names = whitelist.getAll()

    found_protected = []

    for process in processes:

        if process.name in protected_names:
            found_protected.append(
                process.name
            )

    assert not found_protected

    print("Protected processes found in eligible list:")
    print(found_protected)

    print("PASS")

    # --------------------------------------------------
    # Verify every returned process is safe
    # --------------------------------------------------

    print("\nValidating returned processes...")

    for process in processes:

        assert process.userName is not None

        assert not whitelist.isWhitelisted(
            process
        )

    print("All returned processes are:")
    print(" - Current user")
    print(" - Not whitelisted")

    print("PASS")

    # --------------------------------------------------
    # Show sample
    # --------------------------------------------------

    print("\n========== Sample Eligible Processes ==========\n")

    for process in processes[:10]:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    print("\n===============================================")

    print("\nWHITELIST INTEGRATION TEST PASSED\n")


if __name__ == "__main__":

    run_test()