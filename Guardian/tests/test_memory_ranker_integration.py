from Guardian.CandidateSelector import CandidateSelect
from Guardian.MemoryRanker import MemoryRanker


def run_test():

    print("\n========== Memory Ranker Integration ==========\n")

    # --------------------------------------------------
    # 1. Create components
    # --------------------------------------------------

    print("Creating Candidate Selector...")

    selector = CandidateSelect()

    print("PASS")

    print("\nCreating Memory Ranker...")

    ranker = MemoryRanker()

    print("PASS")

    # --------------------------------------------------
    # 2. Get real candidates
    # --------------------------------------------------

    print("\nReading real candidate processes...")

    candidates = selector.getCandidates()

    print(
        f"Candidates Found : {len(candidates)}"
    )

    assert len(candidates) > 0

    print("PASS")

    # --------------------------------------------------
    # 3. Rank real candidates
    # --------------------------------------------------

    print("\nRanking candidates by RAM...")

    ranked = ranker.rank(candidates)

    assert len(ranked) == len(candidates)

    print("PASS")

    # --------------------------------------------------
    # 4. Verify descending RAM order
    # --------------------------------------------------

    print("\nValidating RAM ranking...")

    for index in range(len(ranked) - 1):

        current = ranked[index]
        next_process = ranked[index + 1]

        assert (
            current.memoryBytes
            >=
            next_process.memoryBytes
        )

    print("RAM ranking is correctly descending.")
    print("PASS")

    # --------------------------------------------------
    # 5. Test Top 10
    # --------------------------------------------------

    print("\nSelecting Top 10 RAM consumers...")

    top_processes = ranker.topdetail(
        candidates,
        10
    )

    assert len(top_processes) <= 10

    assert len(top_processes) <= len(
        candidates
    )

    print("PASS")

    # --------------------------------------------------
    # 6. Display results
    # --------------------------------------------------

    print("\n========== Top RAM Consumers ==========\n")

    for process in top_processes:

        print(
            f"PID={process.pid:<8} "
            f"Name={process.name:<25} "
            f"RAM={process.memoryMb:>8.2f} MB "
            f"Status={process.status}"
        )

    print("\n=======================================")

    print("\nMEMORY RANKER INTEGRATION PASSED\n")


if __name__ == "__main__":

    run_test()