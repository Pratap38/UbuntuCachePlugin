from Guardian.RAMMonitor import RamMonitor
from Guardian.MemoryPressureDetector import MemoryPressureCheck
from Guardian.NotificationManager import NotificationManager


def run_test():

    print("\n========== Notification Integration ==========\n")

    monitor = RamMonitor()
    checker = MemoryPressureCheck()
    notifier = NotificationManager()

    # --------------------------------------------------

    print("Reading live RAM...")

    memory = monitor.collect()

    print("PASS")

    # --------------------------------------------------

    print("\nAnalyzing pressure...")

    state = checker.analyze(memory)

    print("PASS")

    # --------------------------------------------------

    print("\n========== LIVE MEMORY ==========\n")

    print(f"RAM Usage : {memory.ramPercent:.1f}%")
    print(f"State     : {state}")

    # --------------------------------------------------
    # Early warning first
    # --------------------------------------------------

    if notifier.earlyWarning(memory.ramPercent):

        print("\nEarly warning notification sent.")

    # --------------------------------------------------
    # State notification
    # --------------------------------------------------

    if notifier.notify(state, memory.ramPercent):

        print("Pressure notification sent.")

    else:

        print("No notification required.")

    # --------------------------------------------------

    print("\n================================")

    print("\nNOTIFICATION INTEGRATION PASSED\n")


if __name__ == "__main__":
    run_test()