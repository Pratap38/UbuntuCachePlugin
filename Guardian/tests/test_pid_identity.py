import os
import tempfile
from datetime import datetime

import psutil

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== PID IDENTITY SAFETY TEST ==========\n"
    )

    # --------------------------------------------------
    # Use this test process as the real process identity
    # --------------------------------------------------

    current = psutil.Process(
        os.getpid()
    )

    pid = current.pid

    startTime = current.create_time()

    print(
        f"Current PID         : {pid}"
    )

    print(
        f"Process Start Time  : {startTime}"
    )

    print("PASS")

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        registry = PauseRegistry(
            stateFile=stateFile
        )

        # --------------------------------------------------
        # Register real identity
        # --------------------------------------------------

        print(
            "\nRegistering process identity..."
        )

        record = PauseProcess(
            pid=pid,
            name=current.name(),
            pausedAt=datetime.now(),
            reason="RAM Critical",
            processStartTime=startTime
        )

        assert registry.add(
            record
        )

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Correct identity
        # --------------------------------------------------

        print(
            "\nTesting correct process identity..."
        )

        assert registry.isSameProcess(
            pid
        )

        print(
            "PID matches."
        )

        print(
            "Start time matches."
        )

        print(
            "Identity → VERIFIED"
        )

        print("PASS")

        # --------------------------------------------------
        # Simulate PID reuse
        # --------------------------------------------------

        print(
            "\nTesting simulated PID reuse..."
        )

        stored = registry.get(
            pid
        )

        assert stored is not None

        originalStartTime = (
            stored.processStartTime
        )

        # Temporarily replace stored identity
        # with a different start time.

        stored.processStartTime = (
            originalStartTime + 1000.0
        )

        assert not registry.isSameProcess(
            pid
        )

        print(
            "PID matches but start time differs."
        )

        print(
            "Identity → REJECTED"
        )

        print("PASS")

        # --------------------------------------------------
        # Restore
        # --------------------------------------------------

        stored.processStartTime = (
            originalStartTime
        )

        assert registry.isSameProcess(
            pid
        )

        print(
            "\nOriginal identity restored."
        )

        print(
            "Identity → VERIFIED"
        )

        print("PASS")

    print(
        "\n=============================================="
    )

    print(
        "\nPID IDENTITY SAFETY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()