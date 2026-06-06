import os

from core.logger import logger
from Scanner.CacheCategory import cacheCategory
from core.constants import CACHE_CATEGORIES



## scan karega apna folder sab
def scanDirectory(path):

    totalSize = 0
    totalFiles = 0

    expandedPath = os.path.expanduser(path)

    logger.info(f"Started scanning: {expandedPath}")

    try:

        for root, dirs, files in os.walk(expandedPath):

            for file in files:

                filePath = os.path.join(root, file)

                try:

                    if os.path.exists(filePath):

                        totalSize += os.path.getsize(filePath)
                        totalFiles += 1

                except PermissionError:

                    logger.warning(f"Permission denied: {filePath}")

                except FileNotFoundError:

                    logger.warning(f"File not found: {filePath}")

    except Exception as e:

        logger.error(f"Scan failed: {e}")

    logger.info(f"Completed scanning: {expandedPath}")

    return totalSize, totalFiles


## scan all category core scanning part hai
def scanAll():

    results = []

    for data in CACHE_CATEGORIES:

        category = cacheCategory(

            data["name"],
            data["path"],
            data["risk"]

        )

        size, files = scanDirectory(category.path)

        category.size = size
        category.files = files

        results.append(category)

    return results

