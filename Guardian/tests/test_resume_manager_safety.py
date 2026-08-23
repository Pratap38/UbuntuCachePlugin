import os
import subprocess
import sys
import time

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager


def run_test():

    print("\n========== Resume Manager Safety Test ==========\n")

    pauseManager = PauseManager()
    resumeManager = ResumeManager()

    # --------------------------------------------------
    # 1. Invalid PID
    # --------------------------------------------------

    print("Testing invalid PID...")

    assert resumeManager.canResume(0) is False

    print("PID=0 → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # 2. Non-existing PID
    # --------------------------------------------------

    print("\nTesting non-existing PID...")

    fakePid = 999999

    assert resumeManager.canResume(fakePid) is False

    print(
        f"PID={fakePid} → REJECTED"
    )
    print("PASS")

    # --------------------------------------------------
    # 3. Current process
    # --------------------------------------------------

    print("\nTesting current process...")

    currentPid = os.getpid()

    assert resumeManager.canResume(
        currentPid
    ) is False

    print(
        f"PID={currentPid} → RUNNING → REJECTED"
    )
    print("PASS")

    # --------------------------------------------------
    # 4. Running process
    # --------------------------------------------------

    print("\nTesting running process...")

    runningProcess = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ]
    )

    try:

        runningPid = runningProcess.pid

        assert resumeManager.canResume(
            runningPid
        ) is False

        print(
            f"PID={runningPid} → RUNNING → REJECTED"
        )
        print("PASS")

    finally:

        runningProcess.terminate()

        try:
            runningProcess.wait(timeout=3)
        except subprocess.TimeoutExpired:
            runningProcess.kill()
            runningProcess.wait()

    # --------------------------------------------------
    # 5. Actually stopped process
    # --------------------------------------------------

    print("\nTesting stopped process...")

    stoppedProcess = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ]
    )

    stoppedPid = stoppedProcess.pid

    try:

        # Actually pause it
        assert pauseManager.pause(
            stoppedPid
        ) is True

        time.sleep(0.5)

        assert pauseManager.isPaused(
            stoppedPid
        )

        # Now ResumeManager should accept it
        assert resumeManager.canResume(
            stoppedPid
        ) is True

        print(
            f"PID={stoppedPid} → STOPPED → ACCEPTED"
        )
        print("PASS")

        # Resume it
        assert resumeManager.resume(
            stoppedPid
        ) is True

        time.sleep(0.5)

        assert resumeManager.isRunning(
            stoppedPid
        )

        print(
            "Stopped process successfully resumed."
        )
        print("PASS")

    finally:

        try:

            if psutil.pid_exists(stoppedPid):

                try:
                    resumeManager.resume(
                        stoppedPid
                    )
                except Exception:
                    pass

                stoppedProcess.terminate()
                stoppedProcess.wait(timeout=3)

        except Exception:

            try:
                stoppedProcess.kill()
            except Exception:
                pass

    print("\n===============================================")

    print(
        "\nRESUME MANAGER SAFETY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()