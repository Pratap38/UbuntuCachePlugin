import time

import psutil

from Guardian.GuardianOrchestrator import GuardianOrchestrator


def run_test():

    print(
        "\n========== REAL GUARDIAN PAUSE PIPELINE ==========\n"
    )

    guardian = GuardianOrchestrator()

    print(
        "Guardian created."
    )

    print("PASS")

    # --------------------------------------------------
    # Run REAL Guardian cycle
    # --------------------------------------------------

    print(
        "\nRunning Guardian against REAL system..."
    )

    result = guardian.runPauseCycle()

    print("PASS")

    memory = result["memory"]
    pressure = result["pressure"]
    process = result["process"]

    # --------------------------------------------------
    # Display live information
    # --------------------------------------------------

    print(
        "\n========== LIVE GUARDIAN DECISION ==========\n"
    )

    print(
        f"RAM Usage       : "
        f"{memory.ramPercent:.1f}%"
    )

    print(
        f"Pressure State  : "
        f"{pressure}"
    )

    print(
        f"Action          : "
        f"{result['action']}"
    )

    print(
        f"Reason          : "
        f"{result['reason']}"
    )

    # --------------------------------------------------
    # No action path
    # --------------------------------------------------

    if not result["action"]:

        print(
            "\nGuardian correctly decided "
            "not to pause a process."
        )

        print(
            f"Reason : {result['reason']}"
        )

        print("PASS")

        print(
            "\n=============================================="
        )

        print(
            "\nREAL GUARDIAN PAUSE PIPELINE PASSED\n"
        )

        return

    # --------------------------------------------------
    # Process was actually selected
    # --------------------------------------------------

    assert process is not None

    print(
        "\n========== SELECTED PROCESS ==========\n"
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

    # --------------------------------------------------
    # Give Linux a moment to update process state
    # --------------------------------------------------

    time.sleep(0.5)

    # --------------------------------------------------
    # Verify actual process state
    # --------------------------------------------------

    print(
        "\nChecking ACTUAL Linux process state..."
    )

    assert psutil.pid_exists(
        process.pid
    )

    assert guardian.pauseManager.isPaused(
        process.pid
    )

    print(
        "Process is actually STOPPED."
    )

    print("PASS")

    # --------------------------------------------------
    # Verify Guardian ownership
    # --------------------------------------------------

    print(
        "\nChecking PauseRegistry..."
    )

    assert guardian.pauseRegistry.contains(
        process.pid
    )

    print(
        "Guardian owns the paused process."
    )

    print("PASS")

    # --------------------------------------------------
    # Verify event history
    # --------------------------------------------------

    print(
        "\nChecking EventHistory..."
    )

    events = guardian.eventHistory.forProcess(
        process.pid
    )

    assert len(events) >= 1

    latest = events[-1]

    assert latest.eventType == "PAUSED"
    assert latest.pid == process.pid

    print(
        f"Event  : {latest.eventType}"
    )

    print(
        f"PID    : {latest.pid}"
    )

    print(
        f"Name   : {latest.processName}"
    )

    print(
        f"RAM    : {latest.ramPercent:.1f}%"
    )

    print(
        f"Reason : {latest.reason}"
    )

    print("PASS")

    print(
        "\n=============================================="
    )

    print(
        "\nREAL GUARDIAN PAUSE PIPELINE PASSED\n"
    )


if __name__ == "__main__":

    run_test()