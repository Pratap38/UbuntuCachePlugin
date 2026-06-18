from concurrent.futures import ThreadPoolExecutor

from Scanner.scan_engine import scanDirectory
from Scanner.CacheCategory import cacheCategory
from core.constants import CACHE_CATEGORIES
import os


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
    max_workers = min(
        len(CACHE_CATEGORIES),
        os.cpu_count() or 1
    )
    with ThreadPoolExecutor(
        max_workers=max_workers
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