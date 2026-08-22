import subprocess
import sys
import time

import psutil

from Guardian.CandidateSelector import CandidateSelect
from Guardian.MemoryRanker import MemoryRanker
from Guardian.DecisionEngine import DecisionEngine
from Guardian.PauseManager import PauseManager
from Guardian.models.PressureState import PressureState


def run_test():

    print("\n========== Pause Manager Integration ==========\n")

    # --------------------------------------------------
    # 1. Create Guardian components
    # --------------------------------------------------

    print("Creating Candidate Selector...")

    selector = CandidateSelect()

    print("PASS")

    print("\nCreating Memory Ranker...")

    ranker = MemoryRanker()

    print("PASS")

    print("\nCreating Decision Engine...")

    decisionEngine = DecisionEngine()

    print("PASS")

    print("\nCreating Pause Manager...")

    pauseManager = PauseManager()

    print("PASS")

    # --------------------------------------------------
    # 2. Create controlled process
    # --------------------------------------------------

    print("\nStarting controlled test process...")

    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ]
    )

    pid = child.pid

    print(f"Test PID : {pid}")
    print("PASS")

    try:

        # --------------------------------------------------
        # 3. Verify process information
        # --------------------------------------------------

        print("\nReading test process...")

        process = psutil.Process(pid)

        assert process.is_running()

        print(
            f"Name   : {process.name()}"
        )

        print(
            f"Status : {process.status()}"
        )

        print("PASS")

        # --------------------------------------------------
        # 4. Candidate safety
        # --------------------------------------------------

        print("\nChecking PauseManager safety...")

        assert pauseManager.canpause(pid)

        print("Test process is safe.")
        print("PASS")

        # --------------------------------------------------
        # 5. Decision Engine
        # --------------------------------------------------

        print("\nTesting critical decision...")

        decision = decisionEngine.decide(
            PressureState.CRITICAL
        )

        assert decision is True

        print(
            "CRITICAL → ACTION REQUIRED"
        )

        print("PASS")

        # --------------------------------------------------
        # 6. Pause selected process
        # --------------------------------------------------

        print("\nPausing selected process...")

        paused = pauseManager.pause(pid)

        assert paused is True

        time.sleep(0.5)

        assert pauseManager.isPaused(pid)

        print(
            "Process successfully paused."
        )

        print("PASS")

        # --------------------------------------------------
        # 7. Resume selected process
        # --------------------------------------------------

        print("\nResuming selected process...")

        resumed = pauseManager.resume(pid)

        assert resumed is True

        time.sleep(0.5)

        assert not pauseManager.isPaused(pid)

        print(
            "Process successfully resumed."
        )

        print("PASS")

    finally:

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        try:

            if psutil.pid_exists(pid):

                try:
                    pauseManager.resume(pid)
                except Exception:
                    pass

                child.terminate()
                child.wait(timeout=3)

        except Exception:

            try:
                child.kill()
            except Exception:
                pass

    print("\n==============================================")

    print(
        "\nPAUSE MANAGER INTEGRATION PASSED\n"
    )


if __name__ == "__main__":

    run_test()