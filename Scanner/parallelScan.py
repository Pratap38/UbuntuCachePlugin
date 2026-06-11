from concurrent.futures import ThreadPoolExecutor

from Scanner.scan_engine import scanDirectory
from Scanner.CacheCategory import cacheCategory
from core.constants import CACHE_CATEGORIES


def scanCategory(data):

    category = cacheCategory(
        data["name"],
        data["path"],
        data["risk"]
    )

    size, files = scanDirectory(
        category.path
    )

    category.size = size
    category.files = files

    return category


def ParallelScan():

    results = []

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        futures = []

        for data in CACHE_CATEGORIES:

            future = executor.submit(
                scanCategory,
                data
            )

            futures.append(future)

        for future in futures:

            results.append(
                future.result()
            )

    return results