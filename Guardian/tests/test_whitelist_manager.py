from Guardian.WhitelistManager import WhitelistManager
from Guardian.GuardianConfig import GuardianConfig


def run_test():

    print("\n========== Whitelist Manager Test ==========\n")

    manager = WhitelistManager()

    # --------------------------------------------------
    # Existing whitelist
    # --------------------------------------------------

    print("Reading whitelist...")

    whitelist = manager.getAll()

    assert isinstance(
        whitelist,
        list
    )

    assert "gnome-shell" in whitelist
    assert "systemd" in whitelist

    print("PASS")

    # --------------------------------------------------
    # Name check
    # --------------------------------------------------

    print("\nTesting protected process...")

    assert manager.isWhitelistedName(
        "gnome-shell"
    )

    print("gnome-shell → WHITELISTED")
    print("PASS")

    # --------------------------------------------------

    print("\nTesting normal process...")

    assert not manager.isWhitelistedName(
        "chrome"
    )

    print("chrome → NOT WHITELISTED")
    print("PASS")

    # --------------------------------------------------
    # Add temporary process
    # --------------------------------------------------

    print("\nTesting add...")

    testName = "RAM-Guardian-Test"

    manager.remove(testName)

    added = manager.add(testName)

    assert added
    assert manager.isWhitelistedName(
        testName
    )

    print("Added successfully")
    print("PASS")

    # --------------------------------------------------
    # Remove temporary process
    # --------------------------------------------------

    print("\nTesting remove...")

    removed = manager.remove(testName)

    assert removed
    assert not manager.isWhitelistedName(
        testName
    )

    print("Removed successfully")
    print("PASS")

    print("\n============================================")

    print("\nWHITELIST MANAGER TEST PASSED\n")


if __name__ == "__main__":

    run_test()