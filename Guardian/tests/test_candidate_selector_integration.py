from Guardian.CandidateSelector import CandidateSelect
from Guardian.WhitelistManager import WhitelistManager


def run_test():

    print("\n========== Candidate Selector Integration ==========\n")

    # --------------------------------------------------
    # 1. Create components
    # --------------------------------------------------

    print("Creating Candidate Selector...")

    selector = CandidateSelect()
    whitelist = WhitelistManager()

    print("PASS")

    # --------------------------------------------------
    # 2. Get candidates from real system
    # --------------------------------------------------

    print("\nReading real system candidates...")

    candidates = selector.getCandidates()

    print(
        f"Candidates Found : {len(candidates)}"
    )

    assert isinstance(
        candidates,
        list
    )

    assert len(candidates) > 0

    print("PASS")

    # --------------------------------------------------
    # 3. Validate candidate safety
    # --------------------------------------------------

    print("\nValidating candidate safety...")

    for process in candidates:

        # Valid PID
        assert process.pid > 0

        # Valid process name
        assert process.name

        # Current user
        assert process.userName == (
            selector.processTracker
            .userProcess()[0].userName
            if selector.processTracker.userProcess()
            else process.userName
        )

        # Valid memory
        assert process.memoryBytes >= 0

        # Must not be whitelisted
        assert not whitelist.isWhitelisted(
            process
        )

    print("All candidates passed safety validation.")

    print("PASS")

    # --------------------------------------------------
    # 4. Verify protected processes are absent
    # --------------------------------------------------

    print("\nChecking protected processes...")

    protected_processes = []

    protected_names = whitelist.getAll()

    for process in candidates:

        if process.name in protected_names:

            protected_processes.append(
                process.name
            )

    print(
        "Protected processes found:"
    )

    print(protected_processes)

    assert not protected_processes

    print("PASS")

    # --------------------------------------------------
    # 5. Display candidate list
    # --------------------------------------------------

    print("\n========== Final Candidate List ==========\n")

    for process in candidates[:15]:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    print("\n==========================================")

    print(
        "\nCANDIDATE SELECTOR "
        "INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()