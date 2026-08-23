import subprocess
import sys
import time

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager


def run_test():

    print("\n========== Pause → Resume Integration ==========\n")

    # --------------------------------------------------
    # 1. Create managers
    # --------------------------------------------------

    print("Creating Pause Manager...")

    pauseManager = PauseManager()

    print("PASS")

    print("\nCreating Resume Manager...")

    resumeManager = ResumeManager()

    print("PASS")

    # --------------------------------------------------
    # 2. Start controlled process
    # --------------------------------------------------

    print("\nStarting controlled test process...")

    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(120)"
        ]
    )

    pid = child.pid

    print(f"Test PID : {pid}")
    print("PASS")

    try:

        process = psutil.Process(pid)

        # --------------------------------------------------
        # 3. Initial state
        # --------------------------------------------------

        print("\n========== Initial State ==========\n")

        assert process.is_running()

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {process.status()}"
        )

        assert process.status() != psutil.STATUS_STOPPED

        print("Process is RUNNING.")
        print("PASS")

        # --------------------------------------------------
        # 4. Pause
        # --------------------------------------------------

        print("\nPausing process...")

        assert pauseManager.canpause(pid)

        assert pauseManager.pause(pid)

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print("Process is STOPPED.")
        print("PASS")

        # --------------------------------------------------
        # 5. Verify Resume Manager detects stopped process
        # --------------------------------------------------

        print("\nChecking Resume Manager...")

        assert resumeManager.canResume(pid)

        print(
            "Resume Manager detected stopped process."
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Resume
        # --------------------------------------------------

        print("\nResuming process...")

        assert resumeManager.resume(pid)

        time.sleep(0.5)

        assert resumeManager.isRunning(pid)

        print("Process is RUNNING again.")
        print("PASS")

        # --------------------------------------------------
        # 7. Final state
        # --------------------------------------------------

        print("\n========== Final State ==========\n")

        process = psutil.Process(pid)

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {process.status()}"
        )

        assert process.status() != psutil.STATUS_STOPPED

        print("Final state verified: RUNNING")
        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            if psutil.pid_exists(pid):

                # Never leave the test process stopped
                try:
                    resumeManager.resume(pid)
                except Exception:
                    pass

                child.terminate()

                try:
                    child.wait(timeout=3)

                except subprocess.TimeoutExpired:

                    child.kill()
                    child.wait()

        except Exception:

            try:
                child.kill()
            except Exception:
                pass

    print("\n==============================================")

    print(
        "\nPAUSE → RESUME INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()