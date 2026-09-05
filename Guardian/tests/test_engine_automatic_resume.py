import subprocess
import sys
import time
from datetime import datetime

import psutil

from Guardian.GuardianEngine import GuardianEngine
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
        "\n========== ENGINE AUTOMATIC RESUME TEST ==========\n"
    )

    print(
        "Creating Guardian Engine..."
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

    try:

        process = psutil.Process(pid)

        # --------------------------------------------------
        # Verify initial state
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

        print(
            "Process is RUNNING."
        )

        print("PASS")

        # --------------------------------------------------
        # Pause REAL process
        # --------------------------------------------------

        print(
            "\n========== PHASE 2: PREPARE GUARDIAN OWNERSHIP ==========\n"
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
        # Register Guardian ownership
        # --------------------------------------------------

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
        # Verify candidate exists at safe RAM
        # --------------------------------------------------

        safeMemory = create_safe_memory()

        print(
            "\n========== PHASE 3: SAFE RAM ==========\n"
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
        # Replace ONLY memory collection
        # --------------------------------------------------

        print(
            "\nInjecting controlled SAFE RAM into engine..."
        )

        engine.orchestrator.ramMonitor.collect = (
            create_safe_memory
        )

        print("PASS")

        # --------------------------------------------------
        # Run REAL Guardian Engine cycle
        # --------------------------------------------------

        print(
            "\n========== PHASE 4: ENGINE RUN CYCLE ==========\n"
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
        # Verify engine resumed process
        # --------------------------------------------------

        print(
            "\n========== PHASE 5: AUTOMATIC RESUME ==========\n"
        )

        resumedProcess = result.get(
            "resumedProcess"
        )

        assert resumedProcess is not None
        assert resumedProcess.pid == pid

        print(
            f"PID={pid} → AUTOMATICALLY RESUMED"
        )

        print("PASS")

        # --------------------------------------------------
        # Verify actual Linux process state
        # --------------------------------------------------

        print(
            "\n========== PHASE 6: REAL PROCESS STATE ==========\n"
        )

        time.sleep(0.5)

        assert psutil.pid_exists(pid)

        finalProcess = psutil.Process(pid)

        assert finalProcess.is_running()

        assert not engine.orchestrator.pauseManager.isPaused(
            pid
        )

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : {finalProcess.status()}"
        )

        print(
            "Process is RUNNING."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify registry cleanup
        # --------------------------------------------------

        print(
            "\n========== PHASE 7: REGISTRY ==========\n"
        )

        assert not (
            engine.orchestrator.pauseRegistry.contains(
                pid
            )
        )

        print(
            "Guardian ownership removed."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify result
        # --------------------------------------------------

        print(
            "\n========== PHASE 8: ENGINE RESULT ==========\n"
        )

        assert result["memory"].ramPercent == 75.0

        assert result["resumedProcess"] is not None

        assert result["actionTaken"] is True

        assert result["actionReason"] == (
            "Process resumed"
        )

        print(
            "Engine reported RESUME correctly."
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

                if engine.orchestrator.pauseManager.isPaused(
                    pid
                ):

                    try:
                        engine.orchestrator.resumeManager.resume(
                            pid
                        )
                    except Exception:
                        pass

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

        print(
            "Cleanup completed."
        )

    print(
        "\n=============================================="
    )

    print(
        "\nENGINE AUTOMATIC RESUME TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()
