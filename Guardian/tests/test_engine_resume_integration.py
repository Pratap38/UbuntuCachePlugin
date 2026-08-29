import subprocess
import sys
import time

import psutil

from Guardian.GuardianEngine import GuardianEngine
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== ENGINE RESUME INTEGRATION ==========\n"
    )

    engine = GuardianEngine(
        interval=1.0
    )

    print(
        "Creating Guardian Engine..."
    )

    print("PASS")

    # --------------------------------------------------
    # Create REAL controlled process
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
        # Initial state
        # --------------------------------------------------

        print(
            "\n========== INITIAL STATE ==========\n"
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
        # Pause
        # --------------------------------------------------

        print(
            "\nPausing controlled process..."
        )

        assert engine.orchestrator.pauseManager.pause(
            pid
        )

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

        print(
            "\nRegistering Guardian ownership..."
        )

        record = PauseProcess(
            pid=pid,
            name=process.name(),
            pausedAt=None,
            reason="RAM Critical"
        )

        assert engine.orchestrator.pauseRegistry.add(
            record
        )

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Test safe RAM condition
        # --------------------------------------------------

        safeRam = 75.0

        print(
            "\n========== SAFE RAM ==========\n"
        )

        print(
            f"Resume condition : {safeRam:.1f}%"
        )

        print(
            "75% → SAFE"
        )

        print("PASS")

        # --------------------------------------------------
        # Engine resume
        # --------------------------------------------------

        print(
            "\nRunning Engine resume cycle..."
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

        # --------------------------------------------------
        # Verify actual Linux state
        # --------------------------------------------------

        time.sleep(0.5)

        print(
            "\nChecking actual Linux process state..."
        )

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
            "Process is RUNNING again."
        )

        print("PASS")

        # --------------------------------------------------
        # Registry cleanup
        # --------------------------------------------------

        print(
            "\nChecking PauseRegistry..."
        )

        assert not (
            engine.orchestrator.pauseRegistry
            .contains(pid)
        )

        print(
            "Guardian ownership removed."
        )

        print("PASS")

        # --------------------------------------------------
        # Final
        # --------------------------------------------------

        print(
            "\n=============================================="
        )

        print(
            "\nENGINE RESUME INTEGRATION PASSED\n"
        )

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

                # Never leave the test process stopped
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