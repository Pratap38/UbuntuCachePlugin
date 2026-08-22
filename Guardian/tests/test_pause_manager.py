import os
import sys
import time
import subprocess

import psutil

from Guardian.PauseManager import PauseManager


def run_test():

    print("\n========== Pause Manager Test ==========\n")

    manager = PauseManager()

    # --------------------------------------------------
    # Start a harmless test process
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
        # Check process exists
        # --------------------------------------------------

        print("\nChecking process...")

        assert psutil.pid_exists(pid)

        print("Process exists.")
        print("PASS")

        # --------------------------------------------------
        # Check whether it can be paused
        # --------------------------------------------------

        print("\nChecking pause safety...")

        assert manager.canpause(pid)

        print("Process is safe to pause.")
        print("PASS")

        # --------------------------------------------------
        # Pause
        # --------------------------------------------------

        print("\nPausing test process...")

        result = manager.pause(pid)

        assert result is True

        time.sleep(0.5)

        assert manager.isPaused(pid)

        print("Process successfully paused.")
        print("PASS")

        # --------------------------------------------------
        # Resume
        # --------------------------------------------------

        print("\nResuming test process...")

        result = manager.resume(pid)

        assert result is True

        time.sleep(0.5)

        process = psutil.Process(pid)

        assert process.status() != psutil.STATUS_STOPPED

        print("Process successfully resumed.")
        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            child.terminate()
            child.wait(timeout=3)

        except Exception:

            try:
                child.kill()
            except Exception:
                pass

    print("\n========================================")

    print("\nPAUSE MANAGER TEST PASSED\n")


if __name__ == "__main__":

    run_test()