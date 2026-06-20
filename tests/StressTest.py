import os
import time

from Scanner.parallelScan import ParallelScan


TEST_FOLDER = "stress_test"


def createTestData():

    if not os.path.exists(TEST_FOLDER):

        os.mkdir(TEST_FOLDER)

    print("Creating Test Files...")

    for folder in range(20):

        folderPath = os.path.join(
            TEST_FOLDER,
            f"folder_{folder}"
        )

        os.makedirs(
            folderPath,
            exist_ok=True
        )

        for file in range(500):

            filePath = os.path.join(
                folderPath,
                f"test_{file}.tmp"
            )

            with open(
                filePath,
                "w"
            ) as f:

                f.write(
                    "Ubuntu Cache Cleaner\n"
                    * 20
                )

    print("Test Data Created")


def runStressTest():

    start = time.time()

    results = ParallelScan()

    end = time.time()

    print(
        f"\nScan Time: {end-start:.2f} Seconds"
    )

    print("\nScan Completed Successfully")


createTestData()

runStressTest()