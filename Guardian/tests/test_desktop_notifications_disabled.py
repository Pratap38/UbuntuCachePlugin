import subprocess

from Guardian.GuardianConfig import GuardianConfig
from Guardian.NotificationManager import NotificationManager
from Guardian.models.PressureState import PressureState


print()
print("========== DESKTOP NOTIFICATIONS DISABLED TEST ==========")
print()

config = GuardianConfig()
originalValue = config.get("desktopNotifications", True)

try:

    print("Disabling desktop notifications...")
    config.set("desktopNotifications", False)
    config.update()

    manager = NotificationManager()

    print("PASS")

    print()
    print("========== PHASE 1: SEND DIRECT NOTIFICATION ==========")
    print()

    def failNotifySend(*args, **kwargs):
        raise AssertionError(
            "notify-send should NOT be executed when "
            "desktopNotifications=False"
        )

    originalRun = subprocess.run
    subprocess.run = failNotifySend

    try:

        result = manager.send(
            "RAM Guardian Test",
            "This notification must not appear."
        )

        print(f"send() result : {result}")

        if result is not False:
            raise AssertionError(
                "send() should return False when notifications are disabled."
            )

        print("notify-send was not called.")
        print("PASS")

    finally:

        subprocess.run = originalRun

    print()
    print("========== PHASE 2: WARNING ==========")
    print()

    result = manager.notify(
        PressureState.WARNING,
        85.0
    )

    print(f"notify() result : {result}")

    if result is not False:
        raise AssertionError(
            "WARNING notification should be disabled."
        )

    print("WARNING notification blocked.")
    print("PASS")

    print()
    print("========== PHASE 3: CRITICAL ==========")
    print()

    result = manager.notify(
        PressureState.CRITICAL,
        92.0
    )

    print(f"notify() result : {result}")

    if result is not False:
        raise AssertionError(
            "CRITICAL notification should be disabled."
        )

    print("CRITICAL notification blocked.")
    print("PASS")

    print()
    print("========== PHASE 4: EMERGENCY ==========")
    print()

    result = manager.notify(
        PressureState.EMERGENCY,
        98.0
    )

    print(f"notify() result : {result}")

    if result is not False:
        raise AssertionError(
            "EMERGENCY notification should be disabled."
        )

    print("EMERGENCY notification blocked.")
    print("PASS")

    print()
    print("========== SUMMARY ==========")
    print()

    print("desktopNotifications=False:")
    print("  Direct send() : BLOCKED")
    print("  WARNING       : BLOCKED")
    print("  CRITICAL      : BLOCKED")
    print("  EMERGENCY     : BLOCKED")
    print()
    print("PASS")
    print()
    print("==============================================")
    print()
    print("DESKTOP NOTIFICATIONS DISABLED TEST PASSED")
    print()

finally:

    config.set("desktopNotifications", originalValue)
    config.update()

    print()
    print("Configuration restored.")