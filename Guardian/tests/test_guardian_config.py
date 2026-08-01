"""
===========================================================

RAM Guardian

GuardianConfig Tests

Author : Ubuntu Cache Cleaner Project

===========================================================
"""

from Guardian.GuardianConfig import GuardianConfig


def run_tests():

    print("\n========== Guardian Config Test ==========\n")

    config = GuardianConfig()

    # ---------------------------------------

    print("Testing Config Object...")

    assert isinstance(

        config,

        GuardianConfig

    )

    print("PASS")

    # ---------------------------------------

    print("Testing Config Loaded...")

    assert config.all() is not None

    print("PASS")

    # ---------------------------------------

    print("Testing Warning Threshold...")

    warning = config.get(

        "warningThreshold"

    )

    assert warning == 80

    print("PASS")

    # ---------------------------------------

    print("Testing Critical Threshold...")

    critical = config.get(

        "criticalThreshold"

    )

    assert critical == 90

    print("PASS")

    # ---------------------------------------

    print("Testing Emergency Threshold...")

    emergency = config.get(

        "emergencyThreshold"

    )

    assert emergency == 97

    print("PASS")

    # ---------------------------------------

    print("Testing Update Config...")

    config.set(

        "monitorInterval",

        5

    )

    assert config.get(

        "monitorInterval"

    ) == 5

    print("PASS")

    # ---------------------------------------

    print("Testing Save Config...")

    config.update()

    print("PASS")

    # ---------------------------------------

    print("Testing Reset Config...")

    config.reset()

    assert config.get(

        "monitorInterval"

    ) == 2

    print("PASS")

    # ---------------------------------------

    print("Testing Whitelist...")

    whitelist = config.get(

        "whitelist"

    )

    assert isinstance(

        whitelist,

        list

    )

    assert len(

        whitelist

    ) > 0

    print("PASS")

    # ---------------------------------------

    print("\n========== Current Configuration ==========\n")

    for key, value in config.all().items():

        print(f"{key:<25} : {value}")

    print("\n===========================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()