import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.GuardianEngine import GuardianEngine
from Guardian.models.PausedProcess import PauseProcess
from Guardian.models.GuardianEvent import GuardianEvent


def run_test():

    print(
        "\n========== FULL GUARDIAN CONTINUOUS CYCLE ==========\n"
    )

    engine = GuardianEngine(
        interval=1.0
    )

    print(
        "Creating Guardian Engine..."
    )

    print("PASS")

    # --------------------------------------------------
    # Start controlled REAL process
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

        # ==================================================
        # PHASE 1 — INITIAL STATE
        # ==================================================

        print(
            "\n========== PHASE 1: INITIAL STATE ==========\n"
        )

        assert process.is_running()

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {process.status()}"
        )

        print(
            "Process is RUNNING."
        )

        print("PASS")

        # ==================================================
        # PHASE 2 — PAUSE
        # ==================================================

        print(
            "\n========== PHASE 2: PAUSE ==========\n"
        )

        paused = (
            engine.orchestrator.pauseManager.pause(
                pid
            )
        )

        assert paused is True

        time.sleep(0.5)

        assert (
            engine.orchestrator.pauseManager
            .isPaused(pid)
        )

        print(
            "Process is STOPPED."
        )

        print("PASS")

        # --------------------------------------------------
        # Register process
        # --------------------------------------------------

        record = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=datetime.now(),
            reason="RAM Critical",
            processStartTime=process.create_time()
        )

        assert (
            engine.orchestrator.pauseRegistry
            .add(record)
        )

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Record PAUSED event
        # --------------------------------------------------

        pausedEvent = GuardianEvent(
            eventType="PAUSED",
            pid=pid,
            processName=process.name(),
            timestamp=None,
            reason="RAM Critical",
            ramPercent=90.0
        )

        assert (
            engine.orchestrator.eventHistory
            .add(pausedEvent)
        )

        print(
            "PAUSED event recorded."
        )

        print("PASS")

        # ==================================================
        # PHASE 3 — INTERVENTION PROTECTION
        # ==================================================

        print(
            "\n========== PHASE 3: INTERVENTION GUARD ==========\n"
        )

        engine.interventionGuard.reset()

        assert (
            engine.interventionGuard
            .canIntervene()
        )

        engine.interventionGuard.recordIntervention()

        assert not (
            engine.interventionGuard
            .canIntervene()
        )

        print(
            "First intervention → ALLOWED"
        )

        print(
            "Second intervention → BLOCKED"
        )

        print("PASS")

        # ==================================================
        # PHASE 4 — NOTIFICATION ANTI-SPAM
        # ==================================================

        print(
            "\n========== PHASE 4: NOTIFICATION ==========\n"
        )

        firstResult = engine.runCycle()

        secondResult = engine.runCycle()

        print(
            f"First notification  : "
            f"{firstResult['notificationSent']}"
        )

        print(
            f"Second notification : "
            f"{secondResult['notificationSent']}"
        )

        # The notification manager may have state from
        # earlier tests. We only require that repeated
        # identical state does not continuously spam.

        if (
            firstResult["pressure"]
            == secondResult["pressure"]
        ):

            assert (
                secondResult["notificationSent"]
                is False
            )

            print(
                "Repeated state → notification suppressed."
            )

        print("PASS")

        # ==================================================
        # PHASE 5 — SAFE RAM
        # ==================================================

        print(
            "\n========== PHASE 5: SAFE RAM ==========\n"
        )

        safeRam = 75.0

        print(
            f"Safe RAM condition : {safeRam:.1f}%"
        )

        candidates = (
            engine.orchestrator
            .resumeCandidateSelector
            .select(safeRam)
        )

        assert len(candidates) == 1

        assert candidates[0].pid == pid

        print(
            f"PID={pid} → RESUME CANDIDATE"
        )

        print("PASS")

        # ==================================================
        # PHASE 6 — RESUME
        # ==================================================

        print(
            "\n========== PHASE 6: RESUME ==========\n"
        )

        resumed = engine.resumeCycle(
            safeRam
        )

        assert resumed is not None

        assert resumed.pid == pid

        print(
            f"PID={pid} → RESUMED"
        )

        print("PASS")

        time.sleep(0.5)

        # --------------------------------------------------
        # Verify actual Linux state
        # --------------------------------------------------

        finalProcess = psutil.Process(pid)

        assert finalProcess.is_running()

        assert not (
            engine.orchestrator.pauseManager
            .isPaused(pid)
        )

        print(
            f"Status : {finalProcess.status()}"
        )

        print(
            "Process is RUNNING again."
        )

        print("PASS")

        # ==================================================
        # PHASE 7 — RESUMED EVENT
        # ==================================================

        print(
            "\n========== PHASE 7: HISTORY ==========\n"
        )

        resumedEvent = GuardianEvent(
            eventType="RESUMED",
            pid=pid,
            processName=finalProcess.name(),
            timestamp=None,
            reason="RAM Normal",
            ramPercent=safeRam
        )

        assert (
            engine.orchestrator.eventHistory
            .add(resumedEvent)
        )

        print(
            "RESUMED event recorded."
        )

        print("PASS")

        # ==================================================
        # PHASE 8 — REGISTRY CLEANUP
        # ==================================================

        print(
            "\n========== PHASE 8: REGISTRY ==========\n"
        )

        assert not (
            engine.orchestrator
            .pauseRegistry
            .contains(pid)
        )

        print(
            "Guardian ownership removed."
        )

        print("PASS")

        # ==================================================
        # PHASE 9 — FINAL HISTORY
        # ==================================================

        print(
            "\n========== PHASE 9: FINAL HISTORY ==========\n"
        )

        events = (
            engine.orchestrator
            .eventHistory
            .forProcess(pid)
        )

        assert len(events) >= 2

        eventTypes = [
            event.eventType
            for event in events
        ]

        assert "PAUSED" in eventTypes
        assert "RESUMED" in eventTypes

        print(
            "PAUSED → RESUMED"
        )

        print(
            f"Total events : {len(events)}"
        )

        print("PASS")

        # ==================================================
        # FINAL STATE
        # ==================================================

        print(
            "\n========== FINAL STATE ==========\n"
        )

        assert finalProcess.is_running()

        assert not (
            engine.orchestrator
            .pauseRegistry
            .contains(pid)
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

        print(
            "\n=============================================="
        )

        print(
            "\nFULL GUARDIAN CONTINUOUS CYCLE PASSED\n"
        )

    finally:

        # ==================================================
        # SAFETY CLEANUP
        # ==================================================

        print(
            "\n========== CLEANUP ==========\n"
        )

        try:

            if psutil.pid_exists(pid):

                process = psutil.Process(pid)

                # Never leave test process stopped
                if (
                    engine.orchestrator
                    .pauseManager
                    .isPaused(pid)
                ):

                    try:
                        engine.orchestrator.resumeManager.resume(pid)
                    except Exception:
                        pass

                try:
                    engine.orchestrator.pauseRegistry.remove(pid)
                except Exception:
                    pass

                process.terminate()

                try:
                    process.wait(timeout=3)

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


if __name__ == "__main__":

    run_test()