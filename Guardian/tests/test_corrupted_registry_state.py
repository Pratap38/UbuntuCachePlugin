import json
import os
import tempfile

from Guardian.PauseRegistry import PauseRegistry


def write_state(path, content):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


def test_case(name, state):

    print(
        f"\nTesting: {name}"
    )

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        write_state(
            stateFile,
            state
        )

        # The registry MUST NOT crash.
        registry = PauseRegistry(
            stateFile=stateFile
        )

        # Invalid state must never produce
        # a trusted process record.
        assert registry.count() == 0

        print(
            "Invalid state rejected safely."
        )

        print("PASS")


def run_test():

    print(
        "\n========== CORRUPTED STATE SAFETY TEST ==========\n"
    )

    # --------------------------------------------------
    # 1. Invalid JSON
    # --------------------------------------------------

    test_case(
        "Invalid JSON",
        "{invalid json"
    )

    # --------------------------------------------------
    # 2. Empty file
    # --------------------------------------------------

    test_case(
        "Empty state file",
        ""
    )

    # --------------------------------------------------
    # 3. JSON list instead of object
    # --------------------------------------------------

    test_case(
        "Wrong root structure",
        "[]"
    )

    # --------------------------------------------------
    # 4. Unsupported version
    # --------------------------------------------------

    test_case(
        "Unsupported version",
        json.dumps({
            "version": 999,
            "processes": []
        })
    )

    # --------------------------------------------------
    # 5. Missing processes
    # --------------------------------------------------

    test_case(
        "Missing processes field",
        json.dumps({
            "version": 1
        })
    )

    # --------------------------------------------------
    # 6. Processes is wrong type
    # --------------------------------------------------

    test_case(
        "Processes wrong type",
        json.dumps({
            "version": 1,
            "processes": {}
        })
    )

    # --------------------------------------------------
    # 7. Invalid PID
    # --------------------------------------------------

    test_case(
        "Invalid PID",
        json.dumps({
            "version": 1,
            "processes": [
                {
                    "pid": -5,
                    "name": "chrome",
                    "pausedAt": "2026-08-31T20:00:00",
                    "reason": "RAM Critical",
                    "processStartTime": 1000.0
                }
            ]
        })
    )

    # --------------------------------------------------
    # 8. Invalid process name
    # --------------------------------------------------

    test_case(
        "Invalid process name",
        json.dumps({
            "version": 1,
            "processes": [
                {
                    "pid": 1001,
                    "name": "",
                    "pausedAt": "2026-08-31T20:00:00",
                    "reason": "RAM Critical",
                    "processStartTime": 1000.0
                }
            ]
        })
    )

    # --------------------------------------------------
    # 9. Invalid pausedAt
    # --------------------------------------------------

    test_case(
        "Invalid pausedAt",
        json.dumps({
            "version": 1,
            "processes": [
                {
                    "pid": 1001,
                    "name": "chrome",
                    "pausedAt": "NOT-A-DATE",
                    "reason": "RAM Critical",
                    "processStartTime": 1000.0
                }
            ]
        })
    )

    # --------------------------------------------------
    # 10. Invalid reason
    # --------------------------------------------------

    test_case(
        "Invalid reason",
        json.dumps({
            "version": 1,
            "processes": [
                {
                    "pid": 1001,
                    "name": "chrome",
                    "pausedAt": "2026-08-31T20:00:00",
                    "reason": None,
                    "processStartTime": 1000.0
                }
            ]
        })
    )

    # --------------------------------------------------
    # 11. Invalid process start time
    # --------------------------------------------------

    test_case(
        "Invalid process start time",
        json.dumps({
            "version": 1,
            "processes": [
                {
                    "pid": 1001,
                    "name": "chrome",
                    "pausedAt": "2026-08-31T20:00:00",
                    "reason": "RAM Critical",
                    "processStartTime": "UNKNOWN"
                }
            ]
        })
    )

    # --------------------------------------------------
    # 12. Mixed valid + invalid records
    # --------------------------------------------------

    print(
        "\nTesting: Mixed valid and invalid records"
    )

    with tempfile.TemporaryDirectory() as tempDir:

        stateFile = os.path.join(
            tempDir,
            "guardian_state.json"
        )

        validProcess = {
            "pid": 1001,
            "name": "chrome",
            "pausedAt": "2026-08-31T20:00:00",
            "reason": "RAM Critical",
            "processStartTime": 1000.0
        }

        invalidProcess = {
            "pid": -99,
            "name": "bad",
            "pausedAt": "invalid",
            "reason": "bad",
            "processStartTime": "bad"
        }

        write_state(
            stateFile,
            json.dumps({
                "version": 1,
                "processes": [
                    validProcess,
                    invalidProcess
                ]
            })
        )

        registry = PauseRegistry(
            stateFile=stateFile
        )

        # Valid record survives.
        assert registry.contains(1001)

        # Invalid record does not.
        assert not registry.contains(-99)

        assert registry.count() == 1

        print(
            "Valid record accepted."
        )

        print(
            "Invalid record rejected."
        )

        print("PASS")

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print(
        "\n=============================================="
    )

    print(
        "\nCORRUPTED STATE SAFETY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()