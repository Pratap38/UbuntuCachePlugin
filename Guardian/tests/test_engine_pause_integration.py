import subprocess
import sys
import time

import psutil

from Guardian.GuardianEngine import GuardianEngine


def run_test():

    print(
        "\n========== ENGINE PAUSE INTEGRATION ==========\n"
    )

    engine = GuardianEngine(
        interval=1.0
    )

    print(
        "Creating Guardian Engine..."
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
        # Create controlled critical decision
        # --------------------------------------------------

        print(
            "\nPreparing controlled critical cycle..."
        )

        # We don't modify your real RAM.
        # We test the intervention path directly.

        engine.interventionGuard.reset()

        # --------------------------------------------------
        # Verify guard initially allows action
        # --------------------------------------------------

        assert (
            engine.interventionGuard.canIntervene()
            is True
        )

        print(
            "InterventionGuard → ALLOWED"
        )

        print("PASS")

        # --------------------------------------------------
        # Directly test orchestrator pause path
        # --------------------------------------------------

        print(
            "\nPausing controlled candidate..."
        )

        candidate = (
            engine.orchestrator
            .candidateSelector
            .createFromProcess(process)
        )

        assert candidate is not None

        success = (
            engine.orchestrator.pauseCandidate(
                candidate,
                ramPercent=90.0,
                reason="RAM Critical"
            )
        )

        assert success is True

        engine.interventionGuard.recordIntervention()

        time.sleep(0.5)

        # --------------------------------------------------
        # Verify actual STOP
        # --------------------------------------------------

        print(
            "\nChecking actual Linux state..."
        )

        assert engine.orchestrator.pauseManager.isPaused(
            pid
        )

        print(
            f"PID    : {pid}"
        )

        print(
            f"Status : "
            f"{psutil.Process(pid).status()}"
        )

        print(
            "Process is actually STOPPED."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify intervention limit
        # --------------------------------------------------

        print(
            "\nChecking intervention protection..."
        )

        assert (
            engine.interventionGuard.canIntervene()
            is False
        )

        print(
            "Second intervention blocked."
        )

        print("PASS")

        # --------------------------------------------------
        # Verify registry
        # --------------------------------------------------

        print(
            "\nChecking PauseRegistry..."
        )

        assert (
            engine.orchestrator.pauseRegistry
            .contains(pid)
        )

        print(
            f"PID={pid} → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Verify history
        # --------------------------------------------------

        print(
            "\nChecking EventHistory..."
        )

        events = (
            engine.orchestrator
            .eventHistory
            .forProcess(pid)
        )

        assert len(events) >= 1

        latest = events[-1]

        assert latest.eventType == "PAUSED"

        print(
            f"Event : {latest.eventType}"
        )

        print(
            f"PID   : {latest.pid}"
        )

        print("PASS")

        print(
            "\n=============================================="
        )

        print(
            "\nENGINE PAUSE INTEGRATION PASSED\n"
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

                # Resume before termination
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

                process = psutil.Process(pid)

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


if __name__ == "__main__":

    run_test()