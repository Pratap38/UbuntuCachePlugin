from Guardian.ResumePolicy import ResumePolicy


def run_test():

    print("\n========== Resume Policy Test ==========\n")

    policy = ResumePolicy()

    threshold = policy.threshold()

    print(
        f"Resume Threshold : {threshold}%"
    )

    # --------------------------------------------------
    # Above threshold
    # --------------------------------------------------

    print("\nTesting unsafe RAM...")

    assert policy.canResume(90.0) is False

    print(
        "90% → DO NOT RESUME"
    )

    print("PASS")

    # --------------------------------------------------
    # Just above threshold
    # --------------------------------------------------

    print("\nTesting RAM just above threshold...")

    assert policy.canResume(75.1) is False

    print(
        "75.1% → DO NOT RESUME"
    )

    print("PASS")

    # --------------------------------------------------
    # Exactly threshold
    # --------------------------------------------------

    print("\nTesting resume threshold...")

    assert policy.canResume(75.0) is True

    print(
        "75% → RESUME ALLOWED"
    )

    print("PASS")

    # --------------------------------------------------
    # Below threshold
    # --------------------------------------------------

    print("\nTesting safe RAM...")

    assert policy.canResume(70.0) is True

    print(
        "70% → RESUME ALLOWED"
    )

    print("PASS")

    # --------------------------------------------------
    # Invalid values
    # --------------------------------------------------

    print("\nTesting invalid RAM values...")

    assert policy.canResume(-1) is False
    assert policy.canResume(101) is False

    print(
        "-1%  → REJECTED"
    )

    print(
        "101% → REJECTED"
    )

    print("PASS")

    print("\n========================================")

    print(
        "\nRESUME POLICY TEST PASSED\n"
    )


if __name__ == "__main__":

    run_test()