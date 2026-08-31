import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime

import psutil

from Guardian.PauseRegistry import PauseRegistry
from Guardian.models.PausedProcess import PauseProcess


def run_test():

    print(
        "\n========== FULL RECOVERY INTEGRATION ==========\n"
    )

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        # ==================================================
        # PHASE 1 — START REAL PROCESS
        # ==================================================

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
            # PHASE 2 — INITIAL STATE
            # ==================================================

            print(
                "\n========== PHASE 1: INITIAL STATE ==========\n"
            )

            assert process.is_running()

            processName = process.name()
            processStartTime = process.create_time()

            print(
                f"PID        : {pid}"
            )

            print(
                f"Name       : {processName}"
            )

            print(
                f"Start Time : {processStartTime}"
            )

            print(
                "Process is RUNNING."
            )

            print("PASS")

            # ==================================================
            # PHASE 3 — GUARDIAN INSTANCE #1
            # ==================================================

            print(
                "\n========== PHASE 2: PAUSE + PERSIST ==========\n"
            )

            registry1 = PauseRegistry(
                stateFile=stateFile
            )

            # --------------------------------------------------
            # Pause
            # --------------------------------------------------

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

            record = PauseProcess(
                pid=pid,
                name=processName,
                pausedAt=datetime.now(),
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
                "Registry persisted to disk."
            )

            print("PASS")

            # ==================================================
            # PHASE 4 — SIMULATE GUARDIAN FAILURE/RESTART
            # ==================================================

            print(
                "\n========== PHASE 3: GUARDIAN RESTART ==========\n"
            )

            del registry1

            print(
                "Guardian Instance #1 stopped."
            )

            print("PASS")

            registry2 = PauseRegistry(
                stateFile=stateFile
            )

            print(
                "Guardian Instance #2 started."
            )

            print("PASS")

            # ==================================================
            # PHASE 5 — RECOVER REGISTRY
            # ==================================================

            print(
                "\n========== PHASE 4: RECOVERY ==========\n"
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
                "Persistent record recovered."
            )

            print("PASS")

            # ==================================================
            # PHASE 6 — IDENTITY VERIFICATION
            # ==================================================

            print(
                "\n========== PHASE 5: IDENTITY ==========\n"
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

            # ==================================================
            # PHASE 7 — PID REUSE PROTECTION
            # ==================================================

            print(
                "\n========== PHASE 6: PID REUSE SAFETY ==========\n"
            )

            originalStartTime = (
                recovered.processStartTime
            )

            recovered.processStartTime = (
                originalStartTime + 9999.0
            )

            assert not registry2.isSameProcess(
                pid
            )

            print(
                "PID matches but identity differs."
            )

            print(
                "Resume safety → REJECTED"
            )

            print("PASS")

            # Restore correct identity.

            recovered.processStartTime = (
                originalStartTime
            )

            assert registry2.isSameProcess(
                pid
            )

            print(
                "Original identity restored."
            )

            print(
                "Resume safety → VERIFIED"
            )

            print("PASS")

            # ==================================================
            # PHASE 8 — RESUME
            # ==================================================

            print(
                "\n========== PHASE 7: SAFE RESUME ==========\n"
            )

            # Final identity check before touching process.

            assert registry2.isSameProcess(
                pid
            )

            process.resume()

            time.sleep(0.5)

            assert process.is_running()

            assert (
                process.status()
                != psutil.STATUS_STOPPED
            )

            print(
                f"PID    : {pid}"
            )

            print(
                f"Status : {process.status()}"
            )

            print(
                "Recovered process successfully resumed."
            )

            print("PASS")

            # ==================================================
            # PHASE 9 — REMOVE OWNERSHIP
            # ==================================================

            print(
                "\n========== PHASE 8: CLEANUP ==========\n"
            )

            assert registry2.remove(
                pid
            )

            assert not registry2.contains(
                pid
            )

            print(
                "Registry ownership removed."
            )

            print("PASS")

            # ==================================================
            # PHASE 10 — PERSISTENT CLEANUP
            # ==================================================

            print(
                "\n========== PHASE 9: PERSISTENT CLEANUP ==========\n"
            )

            registry3 = PauseRegistry(
                stateFile=stateFile
            )

            assert not registry3.contains(
                pid
            )

            assert registry3.count() == 0

            print(
                "Restart after cleanup → registry empty."
            )

            print("PASS")

            # ==================================================
            # FINAL STATE
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
                "Registry is clean."
            )

            print("PASS")

            print(
                "\n=============================================="
            )

            print(
                "\nFULL RECOVERY INTEGRATION PASSED\n"
            )

        finally:

            # ==================================================
            # SAFETY CLEANUP
            # ==================================================

            print(
                "\n========== FINAL PROCESS CLEANUP ==========\n"
            )

            try:

                if psutil.pid_exists(pid):

                    process = psutil.Process(pid)

                    # Never leave the test process stopped.

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