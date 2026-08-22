from Guardian.MemoryRanker import MemoryRanker
from Guardian.models.ProcessInfo import ProcessInfo


def make_process(
    pid,
    name,
    memory_mb
):

    return ProcessInfo(
        pid=pid,
        name=name,
        userName="pratap",
        memoryBytes=memory_mb * 1024 * 1024,
        memoryPercent=1.0,
        status="sleeping"
    )


def run_test():

    print("\n========== Memory Ranker Test ==========\n")

    processes = [

        make_process(
            1001,
            "chrome",
            300
        ),

        make_process(
            1002,
            "code",
            500
        ),

        make_process(
            1003,
            "terminal",
            50
        ),

        make_process(
            1004,
            "firefox",
            250
        )
    ]

    ranker = MemoryRanker()

    # --------------------------------------------------

    print("Ranking processes by RAM...")

    ranked = ranker.rank(processes)

    print("PASS")

    # --------------------------------------------------

    print("\n========== Ranked Processes ==========\n")

    for process in ranked:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<15} "
            f"RAM={process.memoryMb:>8.2f} MB"
        )

    # --------------------------------------------------

    assert ranked[0].name == "code"
    assert ranked[1].name == "chrome"
    assert ranked[2].name == "firefox"
    assert ranked[3].name == "terminal"

    print("\nRanking order verified.")
    print("PASS")

    # --------------------------------------------------

    print("\nTesting Top 2...")

    top = ranker.topdetail(
        processes,
        2
    )

    assert len(top) == 2
    assert top[0].name == "code"
    assert top[1].name == "chrome"

    print("Top 2 verified.")
    print("PASS")

    # --------------------------------------------------

    print("\n======================================")

    print("\nMEMORY RANKER TEST PASSED\n")


if __name__ == "__main__":

    run_test()