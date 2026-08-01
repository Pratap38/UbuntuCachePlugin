from Guardian.RAMMonitor import RamMonitor
from Guardian.models.MemoryInfo import MemoryInfo


def run_tests():

    print("\n========== RAM Guardian Test ==========\n")

    monitor = RamMonitor()

    memory = monitor.collect()

    # -----------------------------------

    print("Testing MemoryInfo Object...")

    assert isinstance(

        memory,

        MemoryInfo

    )

    print("PASS")

    # -----------------------------------

    print("Testing Total RAM...")

    assert memory.totalRam > 0

    print("PASS")

    # -----------------------------------

    print("Testing Used RAM...")

    assert memory.usedRam >= 0

    print("PASS")

    # -----------------------------------

    print("Testing Available RAM...")

    assert memory.availableRam >= 0

    print("PASS")

    # -----------------------------------

    print("Testing Free RAM...")

    assert memory.freeRam >= 0

    print("PASS")

    # -----------------------------------

    print("Testing RAM Percentage...")

    assert 0 <= memory.ramPercent <= 100

    print("PASS")

    # -----------------------------------

    print("Testing Swap Percentage...")

    assert 0 <= memory.swapPercent <= 100

    print("PASS")

    # -----------------------------------

    print("Testing Timestamp...")

    assert memory.timestamp is not None

    print("PASS")

    # -----------------------------------

    print("Testing has_swap()...")

    assert isinstance(

        memory.hasSwap(),

        bool

    )

    print("PASS")

    # -----------------------------------

    print("Testing using_swap()...")

    assert isinstance(

        monitor.UsingSwap(),

        bool

    )

    print("PASS")

    # -----------------------------------

    print("\n========== Memory Snapshot ==========\n")

    print(memory)

    print("\n=====================================")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":

    run_tests()