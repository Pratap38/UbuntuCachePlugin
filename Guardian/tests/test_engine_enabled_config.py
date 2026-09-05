from Guardian.GuardianEngine import GuardianEngine
from Guardian.GuardianConfig import GuardianConfig


def run_tests():

    print("\n========== Guardian Engine Enabled Config Test ==========\n")

    config = GuardianConfig()

    originalEnabled = config.get(
        "enabled",
        True
    )

    try:

        print("Testing enabled=True...")

        config.set(
            "enabled",
            True
        )
        config.update()

        engine = GuardianEngine(
            interval=1.0
        )

        result = engine.runCycle()

        assert result is not None
        assert "actionTaken" in result
        assert "actionReason" in result

        print("PASS")

        print("Testing enabled=False...")

        config.set(
            "enabled",
            False
        )
        config.update()

        engine = GuardianEngine(
            interval=1.0
        )

        result = engine.runCycle()

        assert result is not None
        assert result["decision"] is False
        assert result["notificationSent"] is False
        assert result["actionTaken"] is False
        assert result["actionReason"] == "Guardian disabled"
        assert result["pausedProcess"] is None
        assert result["resumedProcess"] is None

        print("PASS")

    finally:

        config.set(
            "enabled",
            originalEnabled
        )
        config.update()

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":
    run_tests()