import subprocess

from Guardian.GuardianConfig import GuardianConfig
from Guardian.NotificationManager import NotificationManager
from Guardian.models.PressureState import PressureState


print()
print("========== DESKTOP NOTIFICATIONS ENABLED TEST ==========")
print()

config = GuardianConfig()
originalValue = config.get("desktopNotifications", True)

try:

    print("Enabling desktop notifications...")
    config.set("desktopNotifications", True)
    config.update()

    manager = NotificationManager()

    print("PASS")

    print()
    print("========== PHASE 1: WARNING ==========")
    print()

    calls = []

    def fakeRun(command, **kwargs):
        calls.append({
            "command": command,
            "kwargs": kwargs
        })

        class Result:
            returncode = 0

        return Result()

    originalRun = subprocess.run
    subprocess.run = fakeRun

    result = manager.notify(
        PressureState.WARNING,
        85.0
    )

    print(f"notify() result : {result}")
    print(f"subprocess calls: {len(calls)}")

    if result is not True:
        raise AssertionError(
            "WARNING notification should be sent when "
            "desktopNotifications=True."
        )

    if len(calls) != 1:
        raise AssertionError(
            "Expected exactly one notify-send execution."
        )

    command = calls[0]["command"]

    if command[0] != "notify-send":
        raise AssertionError(
            f"Unexpected command: {command}"
        )

    print("notify-send execution allowed.")
    print("PASS")

    print()
    print("========== PHASE 2: REPEATED WARNING ==========")
    print()

    calls.clear()

    result = manager.notify(
        PressureState.WARNING,
        86.0
    )

    print(f"notify() result : {result}")
    print(f"subprocess calls: {len(calls)}")

    if result is not False:
        raise AssertionError(
            "Repeated WARNING should be suppressed."
        )

    if len(calls) != 0:
        raise AssertionError(
            "Repeated WARNING should not call notify-send."
        )

    print("Repeated WARNING suppressed.")
    print("PASS")

    print()
    print("========== PHASE 3: NORMAL RESET ==========")
    print()

    result = manager.notify(
        PressureState.NORMAL,
        70.0
    )

    print(f"notify() result : {result}")

    if result is not False:
        raise AssertionError(
            "NORMAL state should not send a notification."
        )

    print("Notification state reset.")
    print("PASS")

    print()
    print("========== PHASE 4: WARNING AFTER RESET ==========")
    print()

    calls.clear()

    result = manager.notify(
        PressureState.WARNING,
        84.0
    )

    print(f"notify() result : {result}")
    print(f"subprocess calls: {len(calls)}")

    if result is not True:
        raise AssertionError(
            "WARNING should be allowed again after NORMAL reset."
        )

    if len(calls) != 1:
        raise AssertionError(
            "Expected notify-send after notification reset."
        )

    print("WARNING notification allowed after reset.")
    print("PASS")

    print()
    print("========== SUMMARY ==========")
    print()

    print("desktopNotifications=True:")
    print("  WARNING allowed          : PASS")
    print("  notify-send reached      : PASS")
    print("  repeated WARNING blocked : PASS")
    print("  NORMAL reset             : PASS")
    print("  notification after reset: PASS")

    print()
    print("==============================================")
    print()
    print("DESKTOP NOTIFICATIONS ENABLED TEST PASSED")
    print()

finally:

    subprocess.run = originalRun

    config.set("desktopNotifications", originalValue)
    config.update()

    print()
    print("Configuration restored.")