

from datetime import datetime

from Guardian.MemoryPressureDetector import MemoryPressureCheck
from Guardian.models.MemoryInfo import MemoryInfo
from Guardian.models.PressureState import PressureState


def createMemory(ramPercent):

    """
    Creates a fake MemoryInfo object
    for testing.
    """

    return MemoryInfo(

        timestamp=datetime.now(),

        totalRam=8 * 1024 ** 3,

        availableRam=2 * 1024 ** 3,

        usedRam=6 * 1024 ** 3,

        freeRam=2 * 1024 ** 3,

        cacheRam=500 * 1024 ** 2,

        bufferRam=100 * 1024 ** 2,

        ramPercent=ramPercent,

        totalSwap=2 * 1024 ** 3,

        usedSwap=0,

        freeSwap=2 * 1024 ** 3,

        swapPercent=0

    )


def run_tests():

    print("\n========== Memory Pressure Detector Test ==========\n")

    detector = MemoryPressureCheck()

    # --------------------------------------------------

    print("Testing NORMAL State...")

    memory = createMemory(50)

    assert detector.analyze(memory) == PressureState.NORMAL

    assert detector.isNormal(memory)

    print("PASS")

    # --------------------------------------------------

    print("Testing WARNING State...")

    memory = createMemory(82)

    assert detector.analyze(memory) == PressureState.WARNING

    assert detector.isWarning(memory)

    print("PASS")

    # --------------------------------------------------

    print("Testing CRITICAL State...")

    memory = createMemory(92)

    assert detector.analyze(memory) == PressureState.CRITICAL

    assert detector.isCritical(memory)

    print("PASS")

    # --------------------------------------------------

    print("Testing EMERGENCY State...")

    memory = createMemory(99)

    assert detector.analyze(memory) == PressureState.EMERGENCY

    assert detector.isEmergency(memory)

    print("PASS")

    # --------------------------------------------------

    print("Testing PressureState Return Type...")

    memory = createMemory(75)

    state = detector.analyze(memory)

    assert isinstance(

        state,

        PressureState

    )

    print("PASS")

    # --------------------------------------------------

    print("\n========== Detector Summary ==========\n")

    for value in [45, 81, 90, 98]:

        memory = createMemory(value)

        state = detector.analyze(memory)

        print(

            f"RAM : {value}%"

            f"  -->  "

            f"{state}"

        )

    print("\n======================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()
