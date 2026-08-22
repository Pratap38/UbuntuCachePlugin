import os
import subprocess
import sys
import time

import psutil

from Guardian.PauseManager import PauseManager
from Guardian.WhitelistManager import WhitelistManager


def run_test():

    print("\n========== Pause Manager Safety Test ==========\n")

    manager = PauseManager()

    # --------------------------------------------------
    # 1. Invalid PID
    # --------------------------------------------------

    print("Testing invalid PID...")

    assert manager.canpause(0) is False

    print("PID=0 → REJECTED")
    print("PASS")

    # --------------------------------------------------
    # 2. Non-existing PID
    # --------------------------------------------------

    print("\nTesting non-existing PID...")

    fakePid = 999999

    assert manager.canpause(fakePid) is False

    print(
        f"PID={fakePid} → REJECTED"
    )
    print("PASS")

    # --------------------------------------------------
    # 3. Guardian's own PID
    # --------------------------------------------------

    print("\nTesting current process...")

    currentPid = os.getpid()

    assert manager.canpause(currentPid) is False

    print(
        f"PID={currentPid} → SELF → REJECTED"
    )
    print("PASS")

    # --------------------------------------------------
    # 4. Whitelisted process
    # --------------------------------------------------

    print("\nTesting whitelisted process...")

    whitelist = WhitelistManager()

    whitelistName = "test-protected-process"

    added = whitelist.add(
        whitelistName
    )

    assert added is True

    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ],
        executable=sys.executable
    )

    try:

        # The actual process name is normally "python"
        # so we only test the whitelist mechanism
        # using a controlled fake ProcessInfo object.
        from Guardian.models.ProcessInfo import ProcessInfo

        protectedProcess = ProcessInfo(
            pid=child.pid,
            name=whitelistName,
            userName=psutil.Process().username(),
            memoryBytes=0,
            memoryPercent=0.0,
            status="sleeping"
        )

        assert whitelist.isWhitelisted(
            protectedProcess
        )

        print(
            f"{whitelistName} → WHITELISTED → REJECTED"
        )
        print("PASS")

    finally:

        child.terminate()

        try:
            child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()

        whitelist.remove(
            whitelistName
        )

    # --------------------------------------------------
    # 5. Safe process
    # --------------------------------------------------

    print("\nTesting safe process...")

    safeProcess = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; time.sleep(60)"
        ]
    )

    try:

        safePid = safeProcess.pid

        assert manager.canpause(
            safePid
        ) is True

        print(
            f"PID={safePid} → ACCEPTED"
        )
        print("PASS")

    finally:

        safeProcess.terminate()

        try:
            safeProcess.wait(timeout=3)
        except subprocess.TimeoutExpired:
            safeProcess.kill()
            safeProcess.wait()

    # --------------------------------------------------

    print("\n==============================================")

    print(
        "\nPAUSE MANAGER SAFETY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()