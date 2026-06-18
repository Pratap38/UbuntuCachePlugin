import time

from Scanner.parallelScan import ParallelScan

start = time.time()

ParallelScan()

end = time.time()

print(

    f"Scan Time: {end-start:.2f}"

)