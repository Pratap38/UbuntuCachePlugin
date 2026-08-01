
from Guardian.GuardianLogger import GuardLogManager


def run_tests():

    print("\n========== Guardian Logger Test ==========\n")

    logger = GuardLogManager()

    # -----------------------------------------------------

    print("Testing Logger Object...")

    assert isinstance(

        logger,

        GuardLogManager

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing Clear Log...")

    logger.clear()

    assert logger.read() == ""

    print("PASS")

    # -----------------------------------------------------

    print("Testing INFO Log...")

    logger.info(

        "Guardian Started"

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing WARNING Log...")

    logger.warning(

        "Memory Pressure Warning"

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing ERROR Log...")

    logger.error(

        "Notification Service Failed"

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing CRITICAL Log...")

    logger.critical(

        "Emergency Memory Pressure"

    )

    print("PASS")

    # -----------------------------------------------------

    print("Testing Read Log...")

    content = logger.read()

    assert "Guardian Started" in content

    assert "Memory Pressure Warning" in content

    assert "Notification Service Failed" in content

    assert "Emergency Memory Pressure" in content

    print("PASS")

    # -----------------------------------------------------

    print("\n========== Guardian Log ==========\n")

    print(content)

    print("==================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()