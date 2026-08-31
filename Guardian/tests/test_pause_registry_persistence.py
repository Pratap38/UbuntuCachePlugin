import os
import tempfile
from datetime import datetime

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== Pause Registry Persistence Test ==========\n"
    )

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        # --------------------------------------------------
        # Registry A
        # --------------------------------------------------

        print(
            "Creating first registry..."
        )

        registryA = PauseRegistry(
            stateFile=stateFile
        )

        print("PASS")

        # --------------------------------------------------
        # Add process
        # --------------------------------------------------

        process = PauseProcess(
            pid=1001,
            name="chrome",
            pausedAt=datetime.now(),
            reason="RAM Critical"
        )

        print(
            "\nAdding process..."
        )

        assert registryA.add(
            process
        )

        assert registryA.contains(
            1001
        )

        print(
            "PID=1001 → REGISTERED"
        )

        print("PASS")

        # --------------------------------------------------
        # Verify state file
        # --------------------------------------------------

        print(
            "\nChecking persistent state file..."
        )

        assert os.path.exists(
            stateFile
        )

        print(
            "State file created."
        )

        print("PASS")

        # --------------------------------------------------
        # Create NEW registry instance
        # --------------------------------------------------

        print(
            "\nCreating second registry..."
        )

        registryB = PauseRegistry(
            stateFile=stateFile
        )

        print("PASS")

        # --------------------------------------------------
        # Verify recovery
        # --------------------------------------------------

        print(
            "\nChecking recovered process..."
        )

        assert registryB.contains(
            1001
        )

        recovered = registryB.get(
            1001
        )

        assert recovered is not None
        assert recovered.pid == 1001
        assert recovered.name == "chrome"
        assert recovered.reason == "RAM Critical"

        print(
            f"PID    : {recovered.pid}"
        )

        print(
            f"Name   : {recovered.name}"
        )

        print(
            f"Reason : {recovered.reason}"
        )

        print(
            "Process successfully recovered."
        )

        print("PASS")

        # --------------------------------------------------
        # Remove
        # --------------------------------------------------

        print(
            "\nRemoving process..."
        )

        assert registryB.remove(
            1001
        )

        assert not registryB.contains(
            1001
        )

        print(
            "Process removed."
        )

        print("PASS")

        # --------------------------------------------------
        # Create third registry
        # --------------------------------------------------

        print(
            "\nCreating third registry..."
        )

        registryC = PauseRegistry(
            stateFile=stateFile
        )

        print("PASS")

        print(
            "\nChecking persistent removal..."
        )

        assert not registryC.contains(
            1001
        )

        assert registryC.count() == 0

        print(
            "Removed process does not return after restart."
        )

        print("PASS")

    print(
        "\n=============================================="
    )

    print(
        "\nPAUSE REGISTRY PERSISTENCE TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()