from Guardian.DesktopChecker import DesktopChecker
from Guardian.models.DesktopEnvironment import DesktopEnv


def run_tests():

    print("\n========== Desktop Checker Test ==========\n")

    checker = DesktopChecker()

    # --------------------------------------------------

    print("Testing DesktopChecker Object...")

    assert isinstance(

        checker,

        DesktopChecker

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing DesktopEnvironment Object...")

    environment = checker.current()

    assert isinstance(

        environment,

        DesktopEnv

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing Environment Detection...")

    print(

        f"Detected Environment : {environment}"

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing Description...")

    print(

        environment.Description

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing X11 Helper...")

    assert isinstance(

        checker.isX11(),

        bool

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing Wayland Helper...")

    assert isinstance(

        checker.isWayland(),

        bool

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing Unknown Helper...")

    assert isinstance(

        checker.isUnknown(),

        bool

    )

    print("PASS")

    # --------------------------------------------------

    print("Testing Window Tracking Support...")

    assert isinstance(

        checker.supportsWindowTracking(),

        bool

    )

    print("PASS")

    # --------------------------------------------------

    print("\n========== Desktop Report ==========\n")

    print(

        f"Desktop Environment : {environment}"

    )

    print(

        f"Description         : {environment.Description}"

    )

    print(

        f"Supports Tracking   : "

        f"{checker.supportsWindowTracking()}"

    )

    print(

        f"Is X11              : "

        f"{checker.isX11()}"

    )

    print(

        f"Is Wayland          : "

        f"{checker.isWayland()}"

    )

    print(

        f"Is Unknown          : "

        f"{checker.isUnknown()}"

    )

    print("\n====================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()