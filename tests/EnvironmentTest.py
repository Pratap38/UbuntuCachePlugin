from core.EnvironmentChecker import EnvironmentChecker

checker = EnvironmentChecker()

warnings = checker.check()

print("\nEnvironment Check\n")

if warnings:

    for warning in warnings:

        print("Warning:", warning)

else:

    print("Environment OK")
