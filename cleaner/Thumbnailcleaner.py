import os

from cleaner.SafeCleaner import DeleteFolder, DeleteFile
from core.logger import logger


def cleanThumbnailCache():

    thumbnailPath = os.path.expanduser(
        "~/.cache/thumbnails"
    )

    logger.info("Starting thumbnail cache cleaning")

    if not os.path.exists(thumbnailPath):

        logger.warning("Thumbnail cache not found")

        print("Thumbnail cache not found")

        return False

    try:

        failedcount = 0

        for item in os.listdir(thumbnailPath):

            itemPath = os.path.join(
                thumbnailPath,
                item
            )

            if os.path.isdir(itemPath):

                if not DeleteFolder(itemPath):

                    failedcount += 1

            else:

                if not DeleteFile(itemPath):

                    failedcount += 1

        logger.info(
            "Thumbnail cache cleaned successfully"
        )

        print(
            "Thumbnail cache cleaned successfully"
        )

        return failedcount == 0

    except Exception as e:

        logger.error(
            f"Thumbnail cleaning failed: {e}"
        )

        return False