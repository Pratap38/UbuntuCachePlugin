from cleaner.AptCleaner import CleanaptCheck
from cleaner.BrowserClean import cleanBrowserCache
from cleaner.ThrashCleaner import cleanThrash
from cleaner.Thumbnailcleaner import cleanThumbnailCache
from core.logger import logger



def cleanAll():
    logger.info("Complete file cleaning is been starting")

    CleanaptCheck()
    cleanThumbnailCache()
    cleanThrash()
    cleanBrowserCache()

    logger.info("the task succesfully done")
    return True

