import subprocess
import sys

from Guardian.GuardianConfig import GuardianConfig
from Guardian.GuardianOrchestrator import GuardianOrchestrator
from Guardian.models.ProcessInfo import ProcessInfo


print()
print("========== LOG EVENTS DISABLED TEST ==========")
print()

config = GuardianConfig()
originalValue = config.get("logEvents", True)

child = None
pid = None

try:

    print("Disabling event logging...")
    config.set("logEvents", False)
    config.update()
    print("PASS")

    print()
    print("========== PHASE 1: CREATE REAL PROCESS ==========")
    print()

    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(120)"]
    )

    pid = child.pid

    print(f"Test PID : {pid}")

    if not child.poll() is None:
        raise AssertionError("Controlled process did not start.")

    print("Process is RUNNING.")
    print("PASS")

    print()
    print("========== PHASE 2: PAUSE CANDIDATE ==========")
    print()

    orchestrator = GuardianOrchestrator()

    import psutil

    realProcess = psutil.Process(pid)
    memoryInfo = realProcess.memory_info()

    candidate = ProcessInfo(
        pid=realProcess.pid,
        name=realProcess.name(),
        userName=realProcess.username(),
        memoryBytes=memoryInfo.rss,
        memoryPercent=realProcess.memory_percent(),
        status=realProcess.status()
    )

    beforeHistory = orchestrator.eventHistory.count()

    success = orchestrator.pauseCandidate(
        candidate,
        ramPercent=92.0,
        reason="Log Events Disabled Test"
    )

    print(f"pauseCandidate() : {success}")

    if not success:
        raise AssertionError(
            "Process should still pause when logEvents=False."
        )

    print("Guardian pause succeeded.")
    print("PASS")

    print()
    print("========== PHASE 3: VERIFY LINUX STATE ==========")
    print()

    import psutil

    process = psutil.Process(pid)
    status = process.status()

    print(f"PID    : {pid}")
    print(f"Status : {status}")

    if status != psutil.STATUS_STOPPED:
        raise AssertionError(
            "Process should actually be STOPPED."
        )

    print("Process is actually STOPPED.")
    print("PASS")

    print()
    print("========== PHASE 4: VERIFY REGISTRY ==========")
    print()

    if not orchestrator.pauseRegistry.contains(pid):
        raise AssertionError(
            "Paused process should remain in PauseRegistry."
        )

    print(f"PID={pid} → REGISTERED")
    print("PASS")

    print()
    print("========== PHASE 5: VERIFY EVENT HISTORY ==========")
    print()

    afterHistory = orchestrator.eventHistory.count()

    print(f"History before : {beforeHistory}")
    print(f"History after  : {afterHistory}")

    if afterHistory != beforeHistory:
        raise AssertionError(
            "EventHistory should NOT change when "
            "logEvents=False."
        )

    print("No GuardianEvent was recorded.")
    print("PASS")

    print()
    print("========== SUMMARY ==========")
    print()

    print("logEvents=False:")
    print("  Process paused       : PASS")
    print("  Linux process stopped: PASS")
    print("  Registry preserved   : PASS")
    print("  EventHistory unchanged: PASS")

    print()
    print("==============================================")
    print()
    print("LOG EVENTS DISABLED TEST PASSED")
    print()

finally:

    if child is not None:

        try:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=3)
        except Exception:
            pass

    config.set("logEvents", originalValue)
    config.update()

    print()
    print("Configuration restored.")
    print("Cleanup completed.")