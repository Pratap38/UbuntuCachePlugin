
import subprocess
import sys
import time

import psutil

from Guardian.GuardianOrchestrator import GuardianOrchestrator
from Guardian.models.ProcessInfo import ProcessInfo


def run_test():

    print(
        "\n========== Orchestrator Pause Test ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Creating Guardian Orchestrator..."
    )

    print("PASS")

    # --------------------------------------------------
    # Start controlled process
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
        # Build ProcessInfo from REAL process
        # --------------------------------------------------

        memoryInfo = process.memory_info()

        processInfo = ProcessInfo(
            pid=process.pid,
            name=process.name(),
            userName=process.username(),
            memoryBytes=memoryInfo.rss,
            memoryPercent=process.memory_percent(),
            status=process.status()
        )

        # --------------------------------------------------
        # Initial state
        # --------------------------------------------------

        print(
            "\n========== Initial State ==========\n"
        )

        print(
            f"PID    : {processInfo.pid}"
        )

        print(
            f"Name   : {processInfo.name}"
        )

        print(
            f"Status : {processInfo.status}"
        )

        assert process.is_running()

        print(
            "\nProcess is RUNNING."
        )

        print("PASS")

        # --------------------------------------------------
        # Pause through Orchestrator
        # --------------------------------------------------

        print(
            "\nPausing candidate through "
            "GuardianOrchestrator..."
        )

        result = guardian.pauseCandidate(
            processInfo,
            ramPercent=90.5,
            reason="RAM Critical"
        )

        assert result is True

        print(
            "Orchestrator pause returned TRUE."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify actual process state
        # --------------------------------------------------

        print(
            "\nChecking actual process state..."
        )

        time.sleep(0.5)

        assert guardian.pauseManager.isPaused(
            pid
        )

        print(
            f"PID    : {pid}"
        )

        print(
            "Status : STOPPED"
        )

        print(
            "Process is actually paused."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify registry
        # --------------------------------------------------

        print(
            "\nChecking PauseRegistry..."
        )

        assert guardian.pauseRegistry.contains(
            pid
        )

        registered = guardian.pauseRegistry.get(
            pid
        )

        assert registered is not None
        assert registered.pid == pid
        assert registered.name == processInfo.name
        assert registered.reason == "RAM Critical"

        print(
            f"PID    : {registered.pid}"
        )

        print(
            f"Name   : {registered.name}"
        )

        print(
            f"Reason : {registered.reason}"
        )

        print(
            "Process is registered."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify event history
        # --------------------------------------------------

        print(
            "\nChecking EventHistory..."
        )

        events = guardian.eventHistory.forProcess(
            pid
        )

        assert len(events) == 1

        event = events[0]

        assert event.eventType == "PAUSED"
        assert event.pid == pid
        assert event.processName == processInfo.name
        assert event.reason == "RAM Critical"

        print(
            f"Event  : {event.eventType}"
        )

        print(
            f"PID    : {event.pid}"
        )

        print(
            f"Reason : {event.reason}"
        )

        print(
            f"RAM    : {event.ramPercent}%"
        )

        print("PASS")

        # --------------------------------------------------
        # Final verification
        # --------------------------------------------------

        print(
            "\n========== Final State ==========\n"
        )

        assert guardian.pauseManager.isPaused(
            pid
        )

        assert guardian.pauseRegistry.contains(
            pid
        )

        assert guardian.eventHistory.count() == 1

        print(
            "Process       : STOPPED"
        )

        print(
            "Registry      : REGISTERED"
        )

        print(
            "Event History : PAUSED"
        )

        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            if psutil.pid_exists(pid):

                try:
                    guardian.resumeManager.resume(
                        pid
                    )
                except Exception:
                    pass

                guardian.pauseRegistry.remove(
                    pid
                )

                child.terminate()

                try:
                    child.wait(
                        timeout=3
                    )

                except subprocess.TimeoutExpired:

                    child.kill()
                    child.wait()

        except Exception:

            try:
                child.kill()
            except Exception:
                pass

    print(
        "\n=============================================="
    )

    print(
        "\nORCHESTRATOR PAUSE TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()