from Guardian.models.ProcessInfo import ProcessInfo


def run_tests():

    print("\n========== ProcessInfo Test ==========\n")

    process = ProcessInfo(
        pid=14080,
        name="code",
        userName="pratap",
        memoryBytes=650 * 1024 * 1024,
        memoryPercent=4.2,
        status="running"
    )

    assert process.pid == 14080
    assert process.name == "code"
    assert process.memoryMb == 650.0
    assert process.memoryGb > 0
    assert process.status == "running"

    print(process)

    print("\nPROCESS INFO TEST PASSED\n")


if __name__ == "__main__":
    run_tests()