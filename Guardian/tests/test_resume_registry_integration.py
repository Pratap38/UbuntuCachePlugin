import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager
from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== Resume Registry Integration ==========\n"
    )

    pauseManager = PauseManager()
    resumeManager = ResumeManager()
    registry = PauseRegistry()

    # --------------------------------------------------
    # 1. Create real controlled process
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
        # 2. Verify running
        # --------------------------------------------------

        print("\nChecking initial state...")

        assert process.is_running()
        assert not pauseManager.isPaused(pid)

        print("Process is RUNNING.")
        print("PASS")

        # --------------------------------------------------
        # 3. Pause
        # --------------------------------------------------

        print("\nPausing process...")

        assert pauseManager.canpause(pid)
        assert pauseManager.pause(pid)

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print("Process is STOPPED.")
        print("PASS")

        # --------------------------------------------------
        # 4. Register pause
        # --------------------------------------------------

        print("\nRegistering paused process...")

        pausedProcess = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=datetime.now(),
            reason="RAM Critical"
        )

        assert registry.add(
            pausedProcess
        )

        assert registry.contains(pid)

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # 5. Verify ResumeManager safety
        # --------------------------------------------------

        print("\nChecking resume safety...")

        assert resumeManager.canResume(pid)

        print(
            "Process is safe to resume."
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Resume
        # --------------------------------------------------

        print("\nResuming registered process...")

        assert resumeManager.resume(pid)

        time.sleep(0.5)

        assert resumeManager.isRunning(pid)

        print(
            "Process successfully resumed."
        )

        print("PASS")

        # --------------------------------------------------
        # 7. Remove from registry
        # --------------------------------------------------

        print("\nRemoving resumed process from registry...")

        assert registry.remove(pid)

        assert not registry.contains(pid)

        print(
            "Registry entry removed."
        )

        print("PASS")

        # --------------------------------------------------
        # 8. Final verification
        # --------------------------------------------------

        print("\n========== Final State ==========\n")

        process = psutil.Process(pid)

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {process.status()}"
        )

        print(
            f"Registered : {registry.contains(pid)}"
        )

        assert process.status() != psutil.STATUS_STOPPED
        assert not registry.contains(pid)

        print(
            "\nProcess is RUNNING and no longer "
            "owned by the pause registry."
        )

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
        "\nRESUME REGISTRY INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()