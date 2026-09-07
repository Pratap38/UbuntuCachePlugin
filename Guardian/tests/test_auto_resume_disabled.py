import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.GuardianEngine import GuardianEngine
from Guardian.GuardianConfig import GuardianConfig
from Guardian.models.MemoryInfo import MemoryInfo
from Guardian.models.PausedProcess import PauseProcess


def create_safe_memory():
    return MemoryInfo(
        timestamp=datetime.now(),
        totalRam=16 * 1024 * 1024 * 1024,
        availableRam=4 * 1024 * 1024 * 1024,
        usedRam=12 * 1024 * 1024 * 1024,
        freeRam=4 * 1024 * 1024 * 1024,
        cacheRam=0,
        bufferRam=0,
        ramPercent=75.0,
        totalSwap=0,
        usedSwap=0,
        freeSwap=0,
        swapPercent=0.0,
    )


def run_test():

    print(
        "\n========== ENGINE AUTOMATIC RESUME DISABLED TEST ==========\n"
    )

    config = GuardianConfig()

    # Captured BEFORE any mutation, so restoration is correct
    # even if something below fails immediately after.
    originalAutoResume = config.get(
        "autoResume",
        True
    )

    engine = None
    child = None
    pid = None

    try:

        config.set(
            "autoResume",
            False
        )
        config.update()

        print(
            "Creating Guardian Engine (autoResume=False)..."
        )

        engine = GuardianEngine(
            interval=1.0
        )

        print("PASS")

        # --------------------------------------------------
        # Start controlled REAL process
        # --------------------------------------------------

        print(
            "\nStarting controlled REAL process..."
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

        process = psutil.Process(pid)

        # --------------------------------------------------
        # PHASE 1: Verify initial state
        # --------------------------------------------------

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

        print("Process is RUNNING.")

        print("PASS")

        # --------------------------------------------------
        # PHASE 2: Pause the process
        # --------------------------------------------------

        print(
            "\n========== PHASE 2: PAUSE ==========\n"
        )

        paused = engine.orchestrator.pauseManager.pause(
            pid
        )

        assert paused is True

        time.sleep(0.5)

        assert engine.orchestrator.pauseManager.isPaused(
            pid
        )

        print(
            "Process is STOPPED."
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 3: Register in Guardian
        # --------------------------------------------------

        print(
            "\n========== PHASE 3: REGISTER ==========\n"
        )

        pausedRecord = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=datetime.now(),
            reason="RAM Critical",
            processStartTime=process.create_time()
        )

        registered = (
            engine.orchestrator.pauseRegistry.add(
                pausedRecord
            )
        )

        assert registered is True

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 4: Simulate safe RAM
        # --------------------------------------------------

        safeMemory = create_safe_memory()

        print(
            "\n========== PHASE 4: SAFE RAM ==========\n"
        )

        print(
            f"Controlled RAM : "
            f"{safeMemory.ramPercent:.1f}%"
        )

        candidates = (
            engine.orchestrator
            .resumeCandidateSelector
            .select(
                safeMemory.ramPercent
            )
        )

        assert len(candidates) == 1
        assert candidates[0].pid == pid

        print(
            f"PID={pid} → RESUME CANDIDATE"
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 5: Inject controlled memory
        # --------------------------------------------------

        print(
            "\nInjecting controlled SAFE RAM into engine..."
        )

        engine.orchestrator.ramMonitor.collect = (
            create_safe_memory
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 6: Run engine cycle with autoResume=False
        # --------------------------------------------------

        print(
            "\n========== PHASE 6: ENGINE RUN CYCLE ==========\n"
        )

        print(
            "Calling engine.runCycle()..."
        )

        result = engine.runCycle()

        print(
            "runCycle() completed."
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 7: Verify resumedProcess is None
        # --------------------------------------------------

        print(
            "\n========== PHASE 7: VERIFY NO AUTO-RESUME ==========\n"
        )

        resumedProcess = result.get(
            "resumedProcess"
        )

        assert resumedProcess is None

        print(
            f"PID={pid} → NOT RESUMED (autoResume=False)"
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 8: Verify process still STOPPED
        # --------------------------------------------------

        print(
            "\n========== PHASE 8: VERIFY STOPPED STATE ==========\n"
        )

        time.sleep(0.5)

        assert psutil.pid_exists(pid)

        finalProcess = psutil.Process(pid)

        assert engine.orchestrator.pauseManager.isPaused(
            pid
        )

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {finalProcess.status()}"
        )

        print("Process is STOPPED.")

        print("PASS")

        # --------------------------------------------------
        # PHASE 9: Verify registry not cleaned
        # --------------------------------------------------

        print(
            "\n========== PHASE 9: VERIFY REGISTRY ==========\n"
        )

        assert (
            engine.orchestrator.pauseRegistry.contains(
                pid
            )
        )

        print(
            "PID still in PauseRegistry."
        )

        print("PASS")

        # --------------------------------------------------
        # PHASE 10: Summary
        # --------------------------------------------------

        print(
            "\n========== SUMMARY ==========\n"
        )

        print(
            "autoResume=False PREVENTED automatic resume:"
        )

        print(
            f"  resumedProcess    : {resumedProcess}"
        )

        print(
            "  Process status    : STOPPED"
        )

        print(
            "  Registry contains : True"
        )

        print("PASS")

        print(
            "\n=============================================="
        )

        print(
            "\nAUTOMATIC RESUME DISABLED TEST PASSED\n"
        )

    finally:

        # --------------------------------------------------
        # SAFETY CLEANUP
        #
        # Runs no matter where the test above failed —
        # including if GuardianEngine construction itself
        # raised, in which case child/pid were never
        # assigned and are skipped safely.
        # --------------------------------------------------

        print(
            "\n========== CLEANUP ==========\n"
        )

        if child is not None:

            try:

                if psutil.pid_exists(pid):

                    process = psutil.Process(pid)

                    isStopped = False

                    try:
                        isStopped = (
                            engine is not None
                            and engine.orchestrator.pauseManager.isPaused(pid)
                        )
                    except Exception:
                        isStopped = False

                    if isStopped:

                        try:
                            engine.orchestrator.resumeManager.resume(
                                pid
                            )
                        except Exception:
                            pass

                    if engine is not None:

                        try:
                            engine.orchestrator.pauseRegistry.remove(
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

            except Exception:

                try:
                    child.kill()
                except Exception:
                    pass

        # Restore original autoResume value regardless of
        # whether engine construction, process setup, or
        # any assertion above failed.
        config.set(
            "autoResume",
            originalAutoResume
        )
        config.update()

        print(
            "Cleanup completed."
        )


if __name__ == "__main__":

    run_test()
