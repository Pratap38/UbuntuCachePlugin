import os
import subprocess
import sys
import tempfile
import time

import psutil

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== GUARDIAN RESTART RECOVERY ==========\n"
    )

    # --------------------------------------------------
    # Persistent state isolated to this test
    # --------------------------------------------------

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        # --------------------------------------------------
        # Start REAL controlled process
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

            process = psutil.Process(pid)

            # ==================================================
            # GUARDIAN INSTANCE #1
            # ==================================================

            print(
                "\n========== GUARDIAN INSTANCE #1 ==========\n"
            )

            registry1 = PauseRegistry(
                stateFile=stateFile
            )

            print(
                "Guardian Registry #1 created."
            )

            print("PASS")

            # --------------------------------------------------
            # Initial state
            # --------------------------------------------------

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
            # Capture process identity
            # --------------------------------------------------

            processStartTime = (
                process.create_time()
            )

            processName = process.name()

            print(
                "\nCapturing process identity..."
            )

            print(
                f"PID         : {pid}"
            )

            print(
                f"Name        : {processName}"
            )

            print(
                f"Start Time  : {processStartTime}"
            )

            print("PASS")

            # --------------------------------------------------
            # Pause process
            # --------------------------------------------------

            print(
                "\nPausing controlled process..."
            )

            process.suspend()

            time.sleep(0.5)

            assert (
                process.status()
                == psutil.STATUS_STOPPED
            )

            print(
                "Process is STOPPED."
            )

            print("PASS")

            # --------------------------------------------------
            # Register
            # --------------------------------------------------

            print(
                "\nRegistering Guardian ownership..."
            )

            record = PauseProcess(
                pid=pid,
                name=processName,
                pausedAt=__import__(
                    "datetime"
                ).datetime.now(),
                reason="RAM Critical",
                processStartTime=processStartTime
            )

            assert registry1.add(
                record
            )

            print(
                f"PID={pid} → REGISTERED"
            )

            print("PASS")

            # --------------------------------------------------
            # Verify persistence
            # --------------------------------------------------

            assert os.path.exists(
                stateFile
            )

            print(
                "Registry state persisted to disk."
            )

            print("PASS")

            # ==================================================
            # SIMULATE GUARDIAN RESTART
            # ==================================================

            print(
                "\n========== GUARDIAN RESTART ==========\n"
            )

            # Drop first registry instance.
            # The state remains on disk.

            del registry1

            print(
                "Guardian Instance #1 stopped."
            )

            print("PASS")

            # --------------------------------------------------
            # Create second instance
            # --------------------------------------------------

            registry2 = PauseRegistry(
                stateFile=stateFile
            )

            print(
                "Guardian Instance #2 started."
            )

            print("PASS")

            # ==================================================
            # RECOVERY
            # ==================================================

            print(
                "\n========== RECOVERY ==========\n"
            )

            assert registry2.contains(
                pid
            )

            recovered = registry2.get(
                pid
            )

            assert recovered is not None

            print(
                f"PID        : {recovered.pid}"
            )

            print(
                f"Name       : {recovered.name}"
            )

            print(
                f"Reason     : {recovered.reason}"
            )

            print(
                "Paused process successfully recovered."
            )

            print("PASS")

            # --------------------------------------------------
            # Identity verification
            # --------------------------------------------------

            print(
                "\nChecking recovered process identity..."
            )

            assert registry2.isSameProcess(
                pid
            )

            print(
                "PID matches."
            )

            print(
                "Start time matches."
            )

            print(
                "Process identity VERIFIED."
            )

            print("PASS")

            # --------------------------------------------------
            # Verify process remains stopped
            # --------------------------------------------------

            print(
                "\nChecking actual Linux state..."
            )

            assert (
                process.status()
                == psutil.STATUS_STOPPED
            )

            print(
                "Process remains STOPPED."
            )

            print("PASS")

            # ==================================================
            # RESUME AFTER RECOVERY
            # ==================================================

            print(
                "\n========== RESUME AFTER RECOVERY ==========\n"
            )

            process.resume()

            time.sleep(0.5)

            assert process.is_running()

            print(
                "Recovered process successfully resumed."
            )

            print("PASS")

            # --------------------------------------------------
            # Remove registry entry
            # --------------------------------------------------

            assert registry2.remove(
                pid
            )

            assert not registry2.contains(
                pid
            )

            print(
                "Registry entry removed."
            )

            print("PASS")

            # --------------------------------------------------
            # Verify persistent removal
            # --------------------------------------------------

            registry3 = PauseRegistry(
                stateFile=stateFile
            )

            assert not registry3.contains(
                pid
            )

            print(
                "Restart after cleanup → registry empty."
            )

            print("PASS")

            # ==================================================
            # FINAL
            # ==================================================

            print(
                "\n========== FINAL STATE ==========\n"
            )

            assert process.is_running()

            print(
                f"PID        : {pid}"
            )

            print(
                f"Status     : {process.status()}"
            )

            print(
                "Process is RUNNING."
            )

            print(
                "Persistent registry is clean."
            )

            print("PASS")

            print(
                "\n=============================================="
            )

            print(
                "\nGUARDIAN RESTART RECOVERY PASSED\n"
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

                    # Never leave test process stopped.

                    if (
                        process.status()
                        == psutil.STATUS_STOPPED
                    ):

                        try:
                            process.resume()
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


if __name__ == "__main__":

    run_test()