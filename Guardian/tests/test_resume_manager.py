import subprocess
import sys
import time

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager


def run_test():

    print("\n========== Resume Manager Test ==========\n")

    pauseManager = PauseManager()
    resumeManager = ResumeManager()

    # --------------------------------------------------
    # Create controlled test process
    # --------------------------------------------------

    print("Starting test process...")

    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ]
    )

    pid = child.pid

    print(f"Test PID : {pid}")
    print("PASS")

    try:

        # --------------------------------------------------
        # Verify running
        # --------------------------------------------------

        print("\nChecking initial state...")

        assert psutil.Process(pid).is_running()

        print("Process is running.")
        print("PASS")

        # --------------------------------------------------
        # Pause
        # --------------------------------------------------

        print("\nPausing test process...")

        assert pauseManager.pause(pid) is True

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print("Process is paused.")
        print("PASS")

        # --------------------------------------------------
        # Resume safety
        # --------------------------------------------------

        print("\nChecking resume safety...")

        assert resumeManager.canResume(pid) is True

        print("Process is safe to resume.")
        print("PASS")

        # --------------------------------------------------
        # Resume
        # --------------------------------------------------

        print("\nResuming test process...")

        assert resumeManager.resume(pid) is True

        time.sleep(0.5)

        assert resumeManager.isRunning(pid)

        print("Process successfully resumed.")
        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            if psutil.pid_exists(pid):

                try:
                    resumeManager.resume(pid)
                except Exception:
                    pass

                child.terminate()
                child.wait(timeout=3)

        except Exception:

            try:
                child.kill()
            except Exception:
                pass

    print("\n========================================")

    print("\nRESUME MANAGER TEST PASSED\n")


if __name__ == "__main__":

    run_test()