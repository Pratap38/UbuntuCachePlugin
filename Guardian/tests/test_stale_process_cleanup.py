import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== STALE PROCESS CLEANUP TEST ==========\n"
    )

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        # --------------------------------------------------
        # Start real controlled process
        # --------------------------------------------------

        print(
            "Starting controlled REAL process..."
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

            # --------------------------------------------------
            # Create registry
            # --------------------------------------------------

            registry = PauseRegistry(
                stateFile=stateFile
            )

            process = __import__(
                "psutil"
            ).Process(pid)

            processStartTime = (
                process.create_time()
            )

            # --------------------------------------------------
            # Register process
            # --------------------------------------------------

            print(
                "\nRegistering process..."
            )

            record = PauseProcess(
                pid=pid,
                name=process.name(),
                pausedAt=datetime.now(),
                reason="RAM Critical",
                processStartTime=processStartTime
            )

            assert registry.add(
                record
            )

            assert registry.contains(
                pid
            )

            print(
                f"PID={pid} → REGISTERED"
            )

            print("PASS")

            # --------------------------------------------------
            # Kill process
            # --------------------------------------------------

            print(
                "\nTerminating controlled process..."
            )

            process.terminate()

            process.wait(
                timeout=3
            )

            time.sleep(0.2)

            assert not __import__(
                "psutil"
            ).pid_exists(pid)

            print(
                "Process no longer exists."
            )

            print("PASS")

            # --------------------------------------------------
            # Run stale cleanup
            # --------------------------------------------------

            print(
                "\nRunning stale process cleanup..."
            )

            stale = (
                registry.cleanupStaleProcesses()
            )

            assert pid in stale

            print(
                f"PID={pid} → STALE"
            )

            print("PASS")

            # --------------------------------------------------
            # Verify removal
            # --------------------------------------------------

            print(
                "\nChecking registry..."
            )

            assert not registry.contains(
                pid
            )

            assert registry.count() == 0

            print(
                "Stale record removed."
            )

            print("PASS")

            # --------------------------------------------------
            # Verify persistence
            # --------------------------------------------------

            print(
                "\nChecking persistent cleanup..."
            )

            registry2 = PauseRegistry(
                stateFile=stateFile
            )

            assert not registry2.contains(
                pid
            )

            assert registry2.count() == 0

            print(
                "Stale record remains removed after restart."
            )

            print("PASS")

        finally:

            # --------------------------------------------------
            # Safety cleanup
            # --------------------------------------------------

            try:

                if __import__(
                    "psutil"
                ).pid_exists(pid):

                    process = __import__(
                        "psutil"
                    ).Process(pid)

                    process.terminate()

                    try:
                        process.wait(
                            timeout=3
                        )
                    except Exception:
                        process.kill()

            except Exception:
                pass

    print(
        "\n=============================================="
    )

    print(
        "\nSTALE PROCESS CLEANUP TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()