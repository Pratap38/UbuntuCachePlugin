
import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== Pause Registry Integration ==========\n"
    )

    pauseManager = PauseManager()
    registry = PauseRegistry()

    # --------------------------------------------------
    # 1. Start controlled real process
    # --------------------------------------------------

    print("Starting controlled test process...")

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
        # 2. Verify initial state
        # --------------------------------------------------

        print("\nChecking initial process state...")

        assert process.is_running()

        assert process.status() != psutil.STATUS_STOPPED

        print(
            f"Status : {process.status()}"
        )

        print("Process is RUNNING.")
        print("PASS")

        # --------------------------------------------------
        # 3. Safety check
        # --------------------------------------------------

        print("\nChecking pause safety...")

        assert pauseManager.canpause(pid)

        print("Process is safe to pause.")
        print("PASS")

        # --------------------------------------------------
        # 4. Pause real process
        # --------------------------------------------------

        print("\nPausing process...")

        assert pauseManager.pause(pid)

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print("Process successfully paused.")
        print("PASS")

        # --------------------------------------------------
        # 5. Create registry record
        # --------------------------------------------------

        print("\nCreating pause registry record...")

        pausedProcess = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=datetime.now(),
            reason="RAM Critical"
        )

        print(
            f"PID    : {pausedProcess.pid}"
        )

        print(
            f"Name   : {pausedProcess.name}"
        )

        print(
            f"Reason : {pausedProcess.reason}"
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Register actual paused process
        # --------------------------------------------------

        print("\nRegistering paused process...")

        assert registry.add(
            pausedProcess
        )

        print("Process registered.")
        print("PASS")

        # --------------------------------------------------
        # 7. Verify ownership
        # --------------------------------------------------

        print("\nChecking Guardian ownership...")

        assert registry.contains(pid)

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # 8. Retrieve record
        # --------------------------------------------------

        print("\nReading registry record...")

        saved = registry.get(pid)

        assert saved is not None

        assert saved.pid == pid
        assert saved.name == process.name()
        assert saved.reason == "RAM Critical"

        print(
            f"PID    : {saved.pid}"
        )

        print(
            f"Name   : {saved.name}"
        )

        print(
            f"Reason : {saved.reason}"
        )

        print("PASS")

        # --------------------------------------------------
        # 9. Verify process is still paused
        # --------------------------------------------------

        print("\nVerifying process state...")

        assert pauseManager.isPaused(pid)

        print("Process remains STOPPED.")
        print("PASS")

        # --------------------------------------------------
        # 10. Remove registry record
        # --------------------------------------------------

        print("\nRemoving registry record...")

        assert registry.remove(pid)

        assert not registry.contains(pid)

        print("Registry record removed.")
        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            if psutil.pid_exists(pid):

                # Never leave the test process stopped
                try:
                    os_resume = True
                    import os
                    os.kill(pid, 18)
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
        "\nPAUSE REGISTRY INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()