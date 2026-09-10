import os

from Guardian.GuardianPaths import GuardianPaths


print()
print("========== GUARDIAN PATHS TEST ==========")
print()

currentWorkingDirectory = os.getcwd()

configDirectory = GuardianPaths.configDirectory()
configFile = GuardianPaths.configFile()

stateDirectory = GuardianPaths.stateDirectory()
stateFile = GuardianPaths.stateFile()

logDirectory = GuardianPaths.logDirectory()
logFile = GuardianPaths.logFile()


print("Config directory:")
print(configDirectory)

print()
print("Config file:")
print(configFile)

print()
print("State directory:")
print(stateDirectory)

print()
print("State file:")
print(stateFile)

print()
print("Log directory:")
print(logDirectory)

print()
print("Log file:")
print(logFile)


print()
print("========== PHASE 1: ABSOLUTE PATHS ==========")
print()

paths = [
    configDirectory,
    configFile,
    stateDirectory,
    stateFile,
    logDirectory,
    logFile,
]

for path in paths:

    if not path.is_absolute():
        raise AssertionError(
            f"Path is not absolute: {path}"
        )

print("All paths are absolute.")
print("PASS")


print()
print("========== PHASE 2: EXPECTED LOCATIONS ==========")
print()

expectedConfig = (
    GuardianPaths.homeDirectory()
    / ".config"
    / "ubuntu-cache-cleaner"
    / "guardian_config.json"
)

expectedState = (
    GuardianPaths.homeDirectory()
    / ".local"
    / "state"
    / "ubuntu-cache-cleaner"
    / "guardian_state.json"
)

expectedLog = (
    GuardianPaths.homeDirectory()
    / ".local"
    / "state"
    / "ubuntu-cache-cleaner"
    / "logs"
    / "guardian.log"
)


if configFile != expectedConfig:
    raise AssertionError(
        f"Unexpected config path: {configFile}"
    )

if stateFile != expectedState:
    raise AssertionError(
        f"Unexpected state path: {stateFile}"
    )

if logFile != expectedLog:
    raise AssertionError(
        f"Unexpected log path: {logFile}"
    )

print("Config path correct.")
print("State path correct.")
print("Log path correct.")
print("PASS")


print()
print("========== PHASE 3: CWD INDEPENDENCE ==========")
print()

originalDirectory = os.getcwd()

try:

    os.chdir("/tmp")

    if GuardianPaths.configFile() != expectedConfig:
        raise AssertionError(
            "Config path changed with CWD."
        )

    if GuardianPaths.stateFile() != expectedState:
        raise AssertionError(
            "State path changed with CWD."
        )

    if GuardianPaths.logFile() != expectedLog:
        raise AssertionError(
            "Log path changed with CWD."
        )

finally:

    os.chdir(originalDirectory)


print("Paths are independent of current working directory.")
print("PASS")


print()
print("========== PHASE 4: NO FILE CREATION ==========")
print()

if configFile.exists():
    print("WARNING: config file already exists.")

if stateFile.exists():
    print("WARNING: state file already exists.")

if logFile.exists():
    print("WARNING: log file already exists.")

print("Path resolver completed without creating files.")
print("PASS")


print()
print("==============================================")
print()
print("GUARDIAN PATHS TEST PASSED")
print()