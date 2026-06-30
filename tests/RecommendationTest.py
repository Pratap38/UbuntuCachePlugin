from Scanner.parallelScan import ParallelScan

from core.RecommendationEngine import RecommendationEngine


results = ParallelScan()

engine = RecommendationEngine()

recommendations = engine.analyze(

    results

)

print("\nRecommendations\n")

for item in recommendations:

    print(

        f"[{item['level']}]",

        item["title"],

        ":",

        item["message"]

    )