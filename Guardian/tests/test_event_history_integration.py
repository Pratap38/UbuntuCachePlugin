import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.ResumeManager import ResumeManager
from Guardian.PauseRegistry import PauseRegistry
from Guardian.EventHistory import EventHistory
from Guardian.models.PausedProcess import PauseProcess
from Guardian.models.GuardianEvent import GuardianEvent


def run_test():

    print(
        "\n========== Event History Integration ==========\n"
    )

    pauseManager = PauseManager()
    resumeManager = ResumeManager()
    registry = PauseRegistry()
    history = EventHistory()

    # --------------------------------------------------
    # 1. Start real controlled process
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
        # 3. Pause safety
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
        # 5. Register paused process
        # --------------------------------------------------

        print("\nRegistering paused process...")

        pausedAt = datetime.now()

        pausedProcess = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=pausedAt,
            reason="RAM Critical"
        )

        assert registry.add(
            pausedProcess
        )

        assert registry.contains(pid)

        print(
            f"PID    : {pid}"
        )

        print(
            f"Name   : {process.name()}"
        )

        print(
            "Reason : RAM Critical"
        )

        print("Process registered.")
        print("PASS")

        # --------------------------------------------------
        # 6. Record PAUSED event
        # --------------------------------------------------

        print("\nRecording PAUSED event...")

        pausedEvent = GuardianEvent(
            eventType="PAUSED",
            pid=pid,
            processName=process.name(),
            timestamp=pausedAt,
            reason="RAM Critical",
            ramPercent=90.4
        )

        assert history.add(
            pausedEvent
        )

        print("PAUSED event recorded.")
        print("PASS")

        # --------------------------------------------------
        # 7. Verify history
        # --------------------------------------------------

        print("\nChecking PAUSED history...")

        latest = history.latest()

        assert latest is not None
        assert latest.eventType == "PAUSED"
        assert latest.pid == pid

        print(
            f"Event : {latest.eventType}"
        )

        print(
            f"PID   : {latest.pid}"
        )

        print("PASS")

        # --------------------------------------------------
        # 8. Resume safety
        # --------------------------------------------------

        print("\nChecking resume safety...")

        assert resumeManager.canResume(pid)

        print("Process is safe to resume.")
        print("PASS")

        # --------------------------------------------------
        # 9. Resume real process
        # --------------------------------------------------

        print("\nResuming process...")

        assert resumeManager.resume(pid)

        time.sleep(0.5)

        assert resumeManager.isRunning(pid)

        print("Process successfully resumed.")
        print("PASS")

        # --------------------------------------------------
        # 10. Record RESUMED event
        # --------------------------------------------------

        print("\nRecording RESUMED event...")

        resumedAt = datetime.now()

        resumedEvent = GuardianEvent(
            eventType="RESUMED",
            pid=pid,
            processName=process.name(),
            timestamp=resumedAt,
            reason="RAM Normal",
            ramPercent=72.3
        )

        assert history.add(
            resumedEvent
        )

        print("RESUMED event recorded.")
        print("PASS")

        # --------------------------------------------------
        # 11. Remove registry entry
        # --------------------------------------------------

        print("\nRemoving registry entry...")

        assert registry.remove(pid)

        assert not registry.contains(pid)

        print("Registry entry removed.")
        print("PASS")

        # --------------------------------------------------
        # 12. Verify complete history
        # --------------------------------------------------

        print("\n========== COMPLETE EVENT HISTORY ==========\n")

        events = history.forProcess(pid)

        assert len(events) == 2

        assert events[0].eventType == "PAUSED"
        assert events[1].eventType == "RESUMED"

        assert events[0].pid == pid
        assert events[1].pid == pid

        for event in events:

            print(event)

        print("\nEvent order verified:")
        print("PAUSED → RESUMED")
        print("PASS")

        # --------------------------------------------------
        # 13. Final state
        # --------------------------------------------------

        print("\n========== Final State ==========\n")

        process = psutil.Process(pid)

        print(
            f"PID        : {pid}"
        )

        print(
            f"Status     : {process.status()}"
        )

        print(
            f"Registered : {registry.contains(pid)}"
        )

        print(
            f"Events     : {history.count()}"
        )

        assert process.status() != psutil.STATUS_STOPPED
        assert not registry.contains(pid)
        assert history.count() == 2

        print(
            "\nProcess is RUNNING."
        )

        print(
            "Registry no longer owns the process."
        )

        print(
            "History contains PAUSED + RESUMED."
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
        "\nEVENT HISTORY INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()