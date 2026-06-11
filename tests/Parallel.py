
import time

from Scanner.parallelScan import ParallelScan

start = time.time()

results = ParallelScan()

end = time.time()

print(
    f"Scan Time: {end-start:.2f} Seconds"
)

for category in results:

    print(
        category.name,
        category.files
    )