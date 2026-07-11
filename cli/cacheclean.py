import sys
import os

sys.path.insert(

    0,

    os.path.dirname(

        os.path.dirname(

            os.path.abspath(__file__)

        )

    )

)

from ui.CacheSelection import CacheSelectionScreen

from core.EnvironmentChecker import EnvironmentChecker

from core.CrashLogger import CrashLogger


def main():

    checker = EnvironmentChecker()

    warnings = checker.check()

    if warnings:

        print("\nEnvironment Check\n")

        for warning in warnings:

            print(

                f"Warning : {warning}"

            )

        print()

    app = CacheSelectionScreen()

    app.run()


if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        CrashLogger.log(

            e

        )

        print(

            "\nUnexpected Error Occurred."

        )

        print(

            "Crash information has been saved to logs/crash.log"

        )