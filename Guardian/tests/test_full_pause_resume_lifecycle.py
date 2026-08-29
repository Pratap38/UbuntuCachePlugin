import subprocess
import sys
import time

import psutil

from Guardian.GuardianOrchestrator import GuardianOrchestrator
from Guardian.models.PausedProcess import PauseProcess
from Guardian.models.GuardianEvent import GuardianEvent


def run_test():

    print(
        "\n========== FULL PAUSE → RESUME LIFECYCLE ==========\n"
    )

    guardian = GuardianOrchestrator()

    print("Creating Guardian...")
    print("PASS")

    # --------------------------------------------------
    # Start controlled process
    # --------------------------------------------------

    print(
        "\nStarting controlled process..."
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
        # INITIAL STATE
        # --------------------------------------------------

        print(
            "\n========== INITIAL STATE ==========\n"
        )

        assert process.is_running()

        print(
            f"PID    : {pid}"
        )

        print(
            f"Name   : {process.name()}"
        )

        print(
            f"Status : {process.status()}"
        )

        print(
            "Process is RUNNING."
        )

        print("PASS")

        # --------------------------------------------------
        # PAUSE
        # --------------------------------------------------

        print(
            "\n========== PAUSE PHASE ==========\n"
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
        # REGISTER
        # --------------------------------------------------

        print(
            "\nRegistering Guardian ownership..."
        )

        record = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=None,
            reason="RAM Critical"
        )

        assert guardian.pauseRegistry.add(
            record
        )

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # PAUSED EVENT
        # --------------------------------------------------

        print(
            "\nRecording PAUSED event..."
        )

        pausedEvent = GuardianEvent(
            eventType="PAUSED",
            pid=pid,
            processName=process.name(),
            timestamp=None,
            reason="RAM Critical",
            ramPercent=90.0
        )

        assert guardian.eventHistory.add(
            pausedEvent
        )

        print(
            "PAUSED event recorded."
        )

        print("PASS")

        # --------------------------------------------------
        # SAFE CONDITION
        # --------------------------------------------------

        print(
            "\n========== RESUME PHASE ==========\n"
        )

        safeRam = 75.0

        print(
            f"Test safe-RAM condition : "
            f"{safeRam:.1f}%"
        )

        candidates = (
            guardian.resumeCandidateSelector.select(
                safeRam
            )
        )

        assert len(candidates) == 1
        assert candidates[0].pid == pid

        print(
            f"PID={pid} → RESUME CANDIDATE"
        )

        print("PASS")

        # --------------------------------------------------
        # ACTUAL RESUME
        # --------------------------------------------------

        print(
            "\nResuming through Guardian..."
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
        # VERIFY RUNNING
        # --------------------------------------------------

        print(
            "\nChecking actual Linux state..."
        )

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
        # RESUMED EVENT
        # --------------------------------------------------

        print(
            "\nRecording RESUMED event..."
        )

        resumedEvent = GuardianEvent(
            eventType="RESUMED",
            pid=pid,
            processName=finalProcess.name(),
            timestamp=None,
            reason="RAM Normal",
            ramPercent=safeRam
        )

        assert guardian.eventHistory.add(
            resumedEvent
        )

        print(
            "RESUMED event recorded."
        )

        print("PASS")

        # --------------------------------------------------
        # REGISTRY CLEANUP
        # --------------------------------------------------

        print(
            "\nRemoving registry ownership..."
        )

        assert guardian.pauseRegistry.remove(
            pid
        )

        assert not guardian.pauseRegistry.contains(
            pid
        )

        print(
            "Registry entry removed."
        )

        print("PASS")

        # --------------------------------------------------
        # FINAL HISTORY
        # --------------------------------------------------

        print(
            "\n========== FINAL HISTORY ==========\n"
        )

        events = guardian.eventHistory.forProcess(
            pid
        )

        assert len(events) == 2

        assert events[0].eventType == "PAUSED"
        assert events[1].eventType == "RESUMED"

        print(
            "PAUSED → RESUMED"
        )

        print(
            f"Events : {len(events)}"
        )

        print("PASS")

        # --------------------------------------------------
        # FINAL STATE
        # --------------------------------------------------

        print(
            "\n========== FINAL STATE ==========\n"
        )

        assert finalProcess.is_running()

        assert not guardian.pauseRegistry.contains(
            pid
        )

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
            "History    : PAUSED → RESUMED"
        )

        print(
            "Process is RUNNING."
        )

        print(
            "Registry is clean."
        )

        print("PASS")

    finally:

        # --------------------------------------------------
        # HARD SAFETY CLEANUP
        # --------------------------------------------------

        print(
            "\n========== CLEANUP ==========\n"
        )

        try:

            if psutil.pid_exists(pid):

                process = psutil.Process(pid)

                # Never leave test process stopped
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
                    "Controlled process terminated."
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
        "\nFULL PAUSE → RESUME LIFECYCLE PASSED\n"
    )


if __name__ == "__main__":

    run_test()