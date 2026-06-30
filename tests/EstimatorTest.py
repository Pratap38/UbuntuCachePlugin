from Scanner.parallelScan import ParallelScan

from core.CleanTImeEstimatior import CleanupEstimator


results = ParallelScan()

estimator = CleanupEstimator()

estimate = estimator.estimate(

    results

)

print(

    "\nCleanup Estimation\n"

)

print(

    f"Estimated Files : {estimate['files']}"

)

print(

    f"Estimated Space : {estimate['size']}"

)

print(

    f"Estimated Time  : {estimate['seconds']} Seconds"

)
