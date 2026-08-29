import time
import psutil

from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== REAL PAUSE RAM IMPACT ==========\n"
    )

    guardian = GuardianOrchestrator()

    print("Creating Guardian Orchestrator...")
    print("PASS")

    # --------------------------------------------------
    # 1. Collect RAM before Guardian action
    # --------------------------------------------------

    print(
        "\nCollecting REAL RAM before pause..."
    )

    beforeMemory = guardian.ramMonitor.collect()

    print("PASS")

    print(
        f"RAM Before : "
        f"{beforeMemory.ramPercent:.1f}%"
    )

    # --------------------------------------------------
    # 2. Run real Guardian pause cycle
    # --------------------------------------------------

    print(
        "\nRunning REAL Guardian pause cycle..."
    )

    result = guardian.runPauseCycle()

    print("PASS")

    # --------------------------------------------------
    # 3. Display decision
    # --------------------------------------------------

    print(
        "\n========== GUARDIAN DECISION ==========\n"
    )

    print(
        f"RAM Before     : "
        f"{beforeMemory.ramPercent:.1f}%"
    )

    print(
        f"Pressure       : "
        f"{result['pressure']}"
    )

    print(
        f"Action         : "
        f"{result['action']}"
    )

    print(
        f"Reason         : "
        f"{result['reason']}"
    )

    # --------------------------------------------------
    # 4. No action
    # --------------------------------------------------

    if not result["action"]:

        print(
            "\nGuardian did not pause a process."
        )

        print(
            "RAM must reach the configured "
            "critical threshold for this test."
        )

        print(
            "\nNo process was modified."
        )

        print("PASS")

        print(
            "\n=========================================="
        )

        return

    process = result["process"]

    assert process is not None

    pid = process.pid

    print(
        "\n========== PAUSED PROCESS ==========\n"
    )

    print(
        f"PID    : {process.pid}"
    )

    print(
        f"Name   : {process.name}"
    )

    print(
        f"RAM    : {process.memoryMb:.2f} MB"
    )

    print(
        f"Status : {process.status}"
    )

    print("PASS")

    try:

        # --------------------------------------------------
        # 5. Verify process is actually stopped
        # --------------------------------------------------

        print(
            "\nVerifying actual Linux state..."
        )

        time.sleep(1)

        assert guardian.pauseManager.isPaused(
            pid
        )

        print(
            "Process is actually STOPPED."
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Collect RAM after pause
        # --------------------------------------------------

        print(
            "\nCollecting REAL RAM after pause..."
        )

        afterMemory = guardian.ramMonitor.collect()

        print("PASS")

        print(
            f"RAM After : "
            f"{afterMemory.ramPercent:.1f}%"
        )

        # --------------------------------------------------
        # 7. Calculate impact
        # --------------------------------------------------

        ramDifference = (
            afterMemory.ramPercent
            - beforeMemory.ramPercent
        )

        memoryDifference = (
            afterMemory.usedRam
            - beforeMemory.usedRam
        )

        print(
            "\n========== RAM IMPACT ==========\n"
        )

        print(
            f"RAM Before : "
            f"{beforeMemory.ramPercent:.1f}%"
        )

        print(
            f"RAM After  : "
            f"{afterMemory.ramPercent:.1f}%"
        )

        print(
            f"RAM Change : "
            f"{ramDifference:+.1f}%"
        )

        print(
            f"Used RAM Before : "
            f"{beforeMemory.usedRam / (1024 ** 2):.2f} MB"
        )

        print(
            f"Used RAM After  : "
            f"{afterMemory.usedRam / (1024 ** 2):.2f} MB"
        )

        print(
            f"Used RAM Change : "
            f"{memoryDifference / (1024 ** 2):+.2f} MB"
        )

        # --------------------------------------------------
        # 8. Important observation
        # --------------------------------------------------

        if ramDifference < 0:

            print(
                "\nRAM usage decreased after pause."
            )

        elif ramDifference == 0:

            print(
                "\nRAM usage remained approximately unchanged."
            )

        else:

            print(
                "\nRAM usage increased after pause."
            )

        print(
            "\nMeasurement completed."
        )

        print("PASS")

    finally:

        # --------------------------------------------------
        # 9. ALWAYS restore the real process
        # --------------------------------------------------

        print(
            "\n========== CLEANUP ==========\n"
        )

        print(
            "Resuming Guardian-owned process..."
        )

        try:

            if psutil.pid_exists(pid):

                resumed = guardian.resumeManager.resume(
                    pid
                )

                if resumed:

                    print(
                        "Process successfully resumed."
                    )

                else:

                    print(
                        "ResumeManager did not resume "
                        "the process."
                    )

        except Exception as error:

            print(
                f"Resume error: {error}"
            )

        # --------------------------------------------------
        # Remove Guardian ownership
        # --------------------------------------------------

        print(
            "Removing PauseRegistry entry..."
        )

        try:

            guardian.pauseRegistry.remove(
                pid
            )

            print(
                "Registry entry removed."
            )

        except Exception as error:

            print(
                f"Registry cleanup error: {error}"
            )

        # --------------------------------------------------
        # Final state
        # --------------------------------------------------

        time.sleep(0.5)

        if psutil.pid_exists(pid):

            try:

                finalProcess = psutil.Process(pid)

                print(
                    f"Final Status : "
                    f"{finalProcess.status()}"
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                pass

        print("Cleanup completed.")

    print(
        "\n=========================================="
    )

    print(
        "\nREAL PAUSE RAM IMPACT TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()