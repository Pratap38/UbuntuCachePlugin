from datetime import datetime, timedelta

from Guardian.LRUManager import LRU


def run_test():

    print("\n========== LRU Manager Test ==========\n")

    lru = LRU()

    now = datetime.now()

    print("Adding process usage history...")

    lru.update(
        5614,
        now
    )

    lru.update(
        17858,
        now - timedelta(minutes=5)
    )

    lru.update(
        16363,
        now - timedelta(minutes=10)
    )

    print("PASS")

    print("\n========== Least Recently Used ==========\n")

    least_recent = lru.leastRecent()

    print(least_recent)

    assert least_recent == [
        16363,
        17858,
        5614
    ]

    print("PASS")

    print("\n========== Most Recently Used ==========\n")

    most_recent = lru.mostRecent()

    print(most_recent)

    assert most_recent == [
        5614,
        17858,
        16363
    ]

    print("PASS")

    print("\n========== Last Used Timestamp ==========\n")

    timestamp = lru.getLastUsed(5614)

    assert timestamp == now

    print(timestamp)
    print("PASS")

    print("\n========================================")

    print("\nLRU MANAGER TEST PASSED\n")


if __name__ == "__main__":
    run_test()