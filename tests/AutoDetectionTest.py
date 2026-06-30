from Scanner.parallelScan import ParallelScan

from core.AutoDetection import AutoDetectionEngine


results = ParallelScan()

engine = AutoDetectionEngine()

alerts = engine.analazye(

    results

)

print("\nAuto Detection\n")

for alert in alerts:

    print(

        f"[{alert['level']}]",

        alert["title"],

        ":",

        alert["message"]

    )
