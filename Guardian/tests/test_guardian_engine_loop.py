import threading
import time

from Guardian.GuardianEngine import GuardianEngine


def run_test():

    print(
        "\n========== GUARDIAN ENGINE LOOP TEST ==========\n"
    )

    print(
        "Creating Guardian Engine..."
    )

    engine = GuardianEngine(
        interval=0.1
    )

    print("PASS")

    # --------------------------------------------------
    # Controlled cycle counter
    # --------------------------------------------------

    cycleCount = 0

    def controlledCycle():

        nonlocal cycleCount

        cycleCount += 1

        print(
            f"Guardian cycle #{cycleCount}"
        )

        return {
            "memory": None,
            "pressure": None,
            "decision": False,
            "notificationSent": False,
            "actionTaken": False,
            "actionReason": "Test cycle",
            "pausedProcess": None,
            "resumedProcess": None,
        }

    # --------------------------------------------------
    # Replace only runCycle for lifecycle testing
    # --------------------------------------------------

    engine.runCycle = controlledCycle

    print(
        "\nControlled runCycle installed."
    )

    print("PASS")

    # --------------------------------------------------
    # Start engine in test thread
    # --------------------------------------------------

    print(
        "\n========== PHASE 1: START ==========\n"
    )

    engineThread = threading.Thread(
        target=engine.start
    )

    engineThread.start()

    print(
        "Guardian start() launched."
    )

    print("PASS")

    # --------------------------------------------------
    # Allow multiple cycles
    # --------------------------------------------------

    print(
        "\n========== PHASE 2: CONTINUOUS CYCLES ==========\n"
    )

    deadline = time.monotonic() + 3.0

    while (
        cycleCount < 3
        and time.monotonic() < deadline
    ):
        time.sleep(0.05)

    assert cycleCount >= 3

    print(
        f"Cycles executed : {cycleCount}"
    )

    print(
        "Guardian loop is running continuously."
    )

    print("PASS")

    # --------------------------------------------------
    # Stop engine
    # --------------------------------------------------

    print(
        "\n========== PHASE 3: STOP ==========\n"
    )

    engine.stop()

    print(
        "Stop requested."
    )

    print("PASS")

    # --------------------------------------------------
    # Verify thread exits
    # --------------------------------------------------

    print(
        "\n========== PHASE 4: CLEAN SHUTDOWN ==========\n"
    )

    engineThread.join(
        timeout=3.0
    )

    assert not engineThread.is_alive()

    assert engine.running is False

    print(
        "Guardian start() exited cleanly."
    )

    print(
        "Guardian is STOPPED."
    )

    print("PASS")

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    print(
        "\n========== FINAL STATE ==========\n"
    )

    print(
        f"Total cycles : {cycleCount}"
    )

    print(
        f"Running      : {engine.running}"
    )

    print(
        f"Thread alive : {engineThread.is_alive()}"
    )

    assert cycleCount >= 3
    assert engine.running is False
    assert not engineThread.is_alive()

    print(
        "\nContinuous engine lifecycle verified."
    )

    print("PASS")

    print(
        "\n=============================================="
    )

    print(
        "\nGUARDIAN ENGINE LOOP TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()