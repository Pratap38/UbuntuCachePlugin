import subprocess
import sys
import time
import tempfile
from datetime import datetime

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager
from Guardian.PauseRegistry import PauseRegistry
from Guardian.ResumePolicy import ResumePolicy
from Guardian.EventHistory import EventHistory
from Guardian.models.PausedProcess import PauseProcess
from Guardian.models.GuardianEvent import GuardianEvent


def run_test():

    print(
        "\n========== Automatic Resume Integration ==========\n"
    )

    pauseManager = PauseManager()
    resumeManager = ResumeManager()
    registry = PauseRegistry(
        stateFile=tempfile.gettempdir() + "/test_pause_registry.json"
    )
    policy = ResumePolicy()
    history = EventHistory()

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
        # 2. Initial state
        # --------------------------------------------------

        print("\nChecking initial state...")

        assert process.is_running()
        assert not pauseManager.isPaused(pid)

        print(
            f"Name   : {process.name()}"
        )

        print(
            f"Status : {process.status()}"
        )

        print("Process is RUNNING.")
        print("PASS")

        # --------------------------------------------------
        # 3. Pause process
        # --------------------------------------------------

        print("\nPausing process...")

        assert pauseManager.canpause(pid)
        assert pauseManager.pause(pid)

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print("Process is STOPPED.")
        print("PASS")

        # --------------------------------------------------
        # 4. Register process
        # --------------------------------------------------

        print("\nRegistering paused process...")

        pausedAt = datetime.now()

        pausedProcess = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=pausedAt,
            reason="RAM Critical",
            processStartTime=process.create_time()
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
        # 5. Record pause event
        # --------------------------------------------------

        history.add(
            GuardianEvent(
                eventType="PAUSED",
                pid=pid,
                processName=process.name(),
                timestamp=pausedAt,
                reason="RAM Critical",
                ramPercent=90.5
            )
        )

        print(
            "PAUSED event recorded."
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Simulate RAM becoming safe
        # --------------------------------------------------

        safeRam = 75.0

        print(
            f"\nSimulated RAM Usage : {safeRam}%"
        )

        print(
            f"Resume Threshold    : "
            f"{policy.threshold}%"
        )

        assert policy.canResume(
            safeRam
        )

        print(
            "RAM is safe for automatic resume."
        )

        print("PASS")

        # --------------------------------------------------
        # 7. Get Guardian-owned processes
        # --------------------------------------------------

        print(
            "\nChecking Guardian-owned paused processes..."
        )

        pausedProcesses = registry.getAll()

        assert len(pausedProcesses) == 1
        assert pausedProcesses[0].pid == pid

        print(
            f"Guardian paused processes : "
            f"{len(pausedProcesses)}"
        )

        print("PASS")

        # --------------------------------------------------
        # 8. Resume registered process
        # --------------------------------------------------

        print("\nAutomatically resuming process...")

        assert resumeManager.canResume(pid)

        assert resumeManager.resume(pid)

        time.sleep(0.5)

        assert resumeManager.isRunning(pid)

        print(
            "Process successfully resumed."
        )

        print("PASS")

        # --------------------------------------------------
        # 9. Record resume event
        # --------------------------------------------------

        resumedAt = datetime.now()

        history.add(
            GuardianEvent(
                eventType="RESUMED",
                pid=pid,
                processName=process.name(),
                timestamp=resumedAt,
                reason="RAM Normal",
                ramPercent=safeRam
            )
        )

        print(
            "RESUMED event recorded."
        )

        print("PASS")

        # --------------------------------------------------
        # 10. Remove registry entry
        # --------------------------------------------------

        print("\nRemoving registry entry...")

        assert registry.remove(pid)

        assert not registry.contains(pid)

        print(
            "PID removed from PauseRegistry."
        )

        print("PASS")

        # --------------------------------------------------
        # 11. Verify complete lifecycle
        # --------------------------------------------------

        print(
            "\n========== Automatic Resume Result ==========\n"
        )

        events = history.forProcess(pid)

        assert len(events) == 2

        assert events[0].eventType == "PAUSED"
        assert events[1].eventType == "RESUMED"

        print(
            f"PAUSED  : {events[0].timestamp}"
        )

        print(
            f"RESUMED : {events[1].timestamp}"
        )

        print(
            f"PID     : {pid}"
        )

        print(
            f"Status  : {process.status()}"
        )

        print(
            f"Registry: {registry.contains(pid)}"
        )

        assert process.status() != psutil.STATUS_STOPPED
        assert not registry.contains(pid)

        print("\nProcess is RUNNING.")
        print("Registry is clean.")
        print("History contains PAUSED → RESUMED.")

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
        "\nAUTOMATIC RESUME INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()