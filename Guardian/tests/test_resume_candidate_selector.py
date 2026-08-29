from datetime import datetime

from Guardian.ResumeCandidateSelector import (
    ResumeCandidateSelector
)

from Guardian.ResumePolicy import ResumePolicy

from Guardian.PauseRegistry import PauseRegistry

from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== Resume Candidate Selector Test ==========\n"
    )

    registry = PauseRegistry()
    policy = ResumePolicy()

    selector = ResumeCandidateSelector(
        pauseRegistry=registry,
        resumePolicy=policy
    )

    # --------------------------------------------------
    # Add Guardian-owned paused process
    # --------------------------------------------------

    print(
        "Adding Guardian-owned paused process..."
    )

    paused = PauseProcess(
        pid=1001,
        name="chrome",
        pausedAt=datetime.now(),
        reason="RAM Critical"
    )

    assert registry.add(paused)

    print(
        "PID=1001 → REGISTERED"
    )

    print("PASS")

    # --------------------------------------------------
    # RAM still unsafe
    # --------------------------------------------------

    print(
        "\nTesting unsafe RAM..."
    )

    candidates = selector.select(
        80.0
    )

    assert candidates == []

    print(
        "80% → NO RESUME CANDIDATES"
    )

    print("PASS")

    # --------------------------------------------------
    # RAM exactly at threshold
    # --------------------------------------------------

    print(
        "\nTesting resume threshold..."
    )

    candidates = selector.select(
        75.0
    )

    assert len(candidates) == 1
    assert candidates[0].pid == 1001

    print(
        "75% → PID=1001 ACCEPTED"
    )

    print("PASS")

    # --------------------------------------------------
    # RAM below threshold
    # --------------------------------------------------

    print(
        "\nTesting safe RAM..."
    )

    candidates = selector.select(
        70.0
    )

    assert len(candidates) == 1
    assert candidates[0].pid == 1001

    print(
        "70% → PID=1001 ACCEPTED"
    )

    print("PASS")

    # --------------------------------------------------
    # Unregistered process
    # --------------------------------------------------

    print(
        "\nTesting unregistered process..."
    )

    assert not selector.isCandidate(
        9999,
        70.0
    )

    print(
        "PID=9999 → NOT REGISTERED → REJECTED"
    )

    print("PASS")

    # --------------------------------------------------
    # Invalid PID
    # --------------------------------------------------

    print(
        "\nTesting invalid PID..."
    )

    assert not selector.isCandidate(
        0,
        70.0
    )

    print(
        "PID=0 → REJECTED"
    )

    print("PASS")

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print(
        "\n=============================================="
    )

    print(
        "\nRESUME CANDIDATE SELECTOR TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()