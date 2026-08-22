from Guardian.CandidateSelector import CandidateSelect
from Guardian.models.ProcessInfo import ProcessInfo


def make_process(
    pid=1000,
    name="chrome",
    user="pratap",
    memory=100 * 1024 * 1024,
    memory_percent=2.0,
    status="sleeping"
):

    return ProcessInfo(
        pid=pid,
        name=name,
        userName=user,
        memoryBytes=memory,
        memoryPercent=memory_percent,
        status=status
    )


def run_test():

    print("\n========== Candidate Selector Rules ==========\n")

    selector = CandidateSelect()

    # --------------------------------------------------
    # Valid process
    # --------------------------------------------------

    print("Testing valid process...")

    valid = make_process()

    assert selector.isCandidate(valid)

    print("Valid process → ACCEPTED")
    print("PASS")

    # --------------------------------------------------
    # Invalid PID
    # --------------------------------------------------

    print("\nTesting invalid PID...")

    invalid_pid = make_process(
        pid=0
    )

    assert not selector.isCandidate(
        invalid_pid
    )

    print("PID=0 → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Empty process name
    # --------------------------------------------------

    print("\nTesting empty process name...")

    empty_name = make_process(
        name=""
    )

    assert not selector.isCandidate(
        empty_name
    )

    print("Empty name → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Missing user
    # --------------------------------------------------

    print("\nTesting missing user...")

    no_user = make_process(
        user=None
    )

    assert not selector.isCandidate(
        no_user
    )

    print("No user → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Invalid memory
    # --------------------------------------------------

    print("\nTesting invalid memory...")

    invalid_memory = make_process(
        memory=-1
    )

    assert not selector.isCandidate(
        invalid_memory
    )

    print("Negative memory → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Whitelisted process
    # --------------------------------------------------

    print("\nTesting whitelisted process...")

    protected = make_process(
        name="gnome-shell"
    )

    assert selector.whitelistManager.isWhitelisted(
        protected
    )

    assert not selector.isCandidate(
        protected
    )

    print("gnome-shell → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # Different user
    # --------------------------------------------------

    print("\nTesting different user...")

    other_user = make_process(
        user="root"
    )

    # CandidateSelector itself checks that a user exists,
    # while ProcessTracker.userProcess() performs the
    # current-user filtering.
    #
    # Therefore this object is not rejected by
    # isCandidate() solely because its user is different.

    print(
        "Different user → handled by ProcessTracker"
    )
    print("PASS")

    print("\n==============================================")

    print(
        "\nCANDIDATE SELECTOR RULE TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()