from Scanner.parallelScan import ParallelScan

from core. RecommendationEngine import RecommendationEngine


results = ParallelScan()

engine = RecommendationEngine()

recommendations = engine.analyze(
    results
)

print("\nRecommendations\n")

for recommendation in recommendations:

    print(

        "✓",

        recommendation

    )