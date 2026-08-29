import subprocess
import sys
import time

import psutil

from Guardian.GuardianOrchestrator import GuardianOrchestrator
from Guardian.models.PausedProcess import PauseProcess

def run_test():

    print(
        "\n========== REAL AUTOMATIC RESUME PIPELINE ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Creating Guardian Orchestrator..."
    )

    print("PASS")

    # --------------------------------------------------
    # Start a controlled REAL process
    # --------------------------------------------------

    print(
        "\nStarting controlled test process..."
    )

    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(120)"
        ]
    )

    pid = child.pid

    print(
        f"Test PID : {pid}"
    )

    print("PASS")

    try:

        process = psutil.Process(pid)

        # --------------------------------------------------
        # Verify initial state
        # --------------------------------------------------

        print(
            "\n========== Initial State ==========\n"
        )

        print(
            f"PID    : {pid}"
        )

        print(
            f"Name   : {process.name()}"
        )

        print(
            f"Status : {process.status()}"
        )

        assert process.is_running()

        print(
            "Process is RUNNING."
        )

        print("PASS")

        # --------------------------------------------------
        # Pause controlled process
        # --------------------------------------------------

        print(
            "\nPausing controlled process..."
        )

        paused = guardian.pauseManager.pause(
            pid
        )

        assert paused is True

        time.sleep(0.5)

        assert guardian.pauseManager.isPaused(
            pid
        )

        print(
            "Process is STOPPED."
        )

        print("PASS")

        # --------------------------------------------------
        # Register Guardian ownership
        # --------------------------------------------------

        print(
            "\nRegistering paused process..."
        )

        processInfo = process

        pausedRecord = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=None,
            reason="RAM Critical"
        )

        registered = guardian.pauseRegistry.add(
            pausedRecord
        )

        assert registered is True

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Test ResumeCandidateSelector
        # --------------------------------------------------

        print(
            "\nCreating ResumeCandidateSelector..."
        )

        from Guardian.ResumeCandidateSelector import (
            ResumeCandidateSelector
        )

        selector = ResumeCandidateSelector(
            pauseRegistry=guardian.pauseRegistry,
            resumePolicy=guardian.resumePolicy
        )

        print("PASS")

        # --------------------------------------------------
        # Safe RAM condition
        # --------------------------------------------------

        safeRam = 75.0

        print(
            "\n========== Resume Decision ==========\n"
        )

        print(
            f"Simulated RAM : {safeRam:.1f}%"
        )

        print(
            "Resume threshold : 75%"
        )

        candidates = selector.select(
            safeRam
        )

        assert len(candidates) == 1
        assert candidates[0].pid == pid

        print(
            f"PID={pid} → RESUME CANDIDATE"
        )

        print("PASS")

        # --------------------------------------------------
        # Verify process is still stopped
        # --------------------------------------------------

        assert guardian.pauseManager.isPaused(
            pid
        )

        print(
            "Process is still STOPPED before resume."
        )

        print("PASS")

        # --------------------------------------------------
        # Resume through ResumeManager
        # --------------------------------------------------

        print(
            "\nResuming through ResumeManager..."
        )

        resumed = guardian.resumeManager.resume(
            pid
        )

        assert resumed is True

        time.sleep(0.5)

        print(
            "ResumeManager returned TRUE."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify ACTUAL running state
        # --------------------------------------------------

        print(
            "\nChecking actual Linux process state..."
        )

        assert psutil.pid_exists(pid)

        finalProcess = psutil.Process(pid)

        assert finalProcess.is_running()

        assert not guardian.pauseManager.isPaused(
            pid
        )

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {finalProcess.status()}"
        )

        print(
            "Process is RUNNING again."
        )

        print("PASS")

        # --------------------------------------------------
        # Record RESUMED event
        # --------------------------------------------------

        print(
            "\nRecording RESUMED event..."
        )

        # Use the existing EventHistory API.
        # This mirrors the event structure already used
        # by the project's integration tests.

        from Guardian.models.GuardianEvent import GuardianEvent
        from datetime import datetime

        resumedEvent = GuardianEvent(
            eventType="RESUMED",
            pid=pid,
            processName=finalProcess.name(),
            timestamp=datetime.now(),
            reason="RAM Normal",
            ramPercent=safeRam
        )

        added = guardian.eventHistory.add(
            resumedEvent
        )

        assert added is True

        print(
            "RESUMED event recorded."
        )

        print("PASS")

        # --------------------------------------------------
        # Remove registry ownership
        # --------------------------------------------------

        print(
            "\nRemoving PauseRegistry entry..."
        )

        removed = guardian.pauseRegistry.remove(
            pid
        )

        assert removed is True

        print(
            f"PID={pid} → REMOVED"
        )

        print("PASS")

        # --------------------------------------------------
        # Final verification
        # --------------------------------------------------

        print(
            "\n========== Final State ==========\n"
        )

        assert not guardian.pauseRegistry.contains(
            pid
        )

        events = guardian.eventHistory.forProcess(
            pid
        )

        assert len(events) >= 1

        latest = events[-1]

        assert latest.eventType == "RESUMED"
        assert latest.pid == pid

        print(
            f"PID        : {pid}"
        )

        print(
            f"Status     : {finalProcess.status()}"
        )

        print(
            "Registry   : False"
        )

        print(
            f"Latest Event : {latest.eventType}"
        )

        print(
            "Process is RUNNING."
        )

        print(
            "Registry is clean."
        )

        print(
            "RESUMED event verified."
        )

        print("PASS")

    finally:

        # --------------------------------------------------
        # Safety cleanup
        # --------------------------------------------------

        print(
            "\n========== CLEANUP ==========\n"
        )

        try:

            if psutil.pid_exists(pid):

                process = psutil.Process(pid)

                # Never leave our test process stopped.

                if guardian.pauseManager.isPaused(
                    pid
                ):

                    try:
                        guardian.resumeManager.resume(
                            pid
                        )
                    except Exception:
                        pass

                try:
                    guardian.pauseRegistry.remove(
                        pid
                    )
                except Exception:
                    pass

                process.terminate()

                try:
                    process.wait(
                        timeout=3
                    )

                except psutil.TimeoutExpired:

                    process.kill()
                    process.wait()

                print(
                    "Controlled test process terminated."
                )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            pass

        print(
            "Cleanup completed."
        )

    print(
        "\n=============================================="
    )

    print(
        "\nREAL AUTOMATIC RESUME PIPELINE PASSED\n"
    )


if __name__ == "__main__":

    run_test()