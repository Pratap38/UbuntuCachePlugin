from Guardian.CandidateSelector import CandidateSelect
from Guardian.models.ProcessInfo import ProcessInfo


def run_test():

    print("\n========== Candidate Selector Test ==========\n")

    selector = CandidateSelect()

    # --------------------------------------------------
    # Get candidates
    # --------------------------------------------------

    print("Reading candidate processes...")

    candidates = selector.getCandidates()

    print(
        f"Candidates Found : {len(candidates)}"
    )

    assert isinstance(
        candidates,
        list
    )

    print("PASS")

    # --------------------------------------------------
    # Validate every candidate
    # --------------------------------------------------

    print("\nValidating candidates...")

    for process in candidates:

        assert isinstance(
            process,
            ProcessInfo
        )

        assert process.pid > 0

        assert process.name

        assert process.userName is not None

        assert process.memoryBytes >= 0

        assert not selector.whitelistManager.isWhitelisted(
            process
        )

    print("All candidates passed safety checks.")

    print("PASS")

    # --------------------------------------------------
    # Display sample
    # --------------------------------------------------

    print("\n========== Sample Candidates ==========\n")

    for process in candidates[:10]:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    print("\n=======================================")

    print("\nCANDIDATE SELECTOR TEST PASSED\n")


if __name__ == "__main__":

    run_test()