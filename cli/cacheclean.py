import sys
import os
import argparse

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


def parseArgs(argv=None):

    parser = argparse.ArgumentParser(

        prog="cacheclean",

        description="Professional Ubuntu Cache Cleaning Utility"

    )

    parser.add_argument(

        "--version",

        action="store_true",

        help="Show the installed version and exit"

    )

    return parser.parse_args(argv)


def printVersion():

    try:

        from importlib.metadata import version, PackageNotFoundError

        print(f"cacheclean {version('Baker')}")

    except PackageNotFoundError:

        print("cacheclean version unknown (package not installed)")


def main():

    try:

        args = parseArgs()

        if args.version:

            printVersion()

            return

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

        sys.exit(1)


if __name__ == "__main__":

    main()