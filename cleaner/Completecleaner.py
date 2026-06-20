# from cleaner.AptCleaner import CleanaptCheck
# from cleaner.BrowserClean import cleanBrowserCache
# from cleaner.ThrashCleaner import cleanThrash
# from cleaner.Thumbnailcleaner import cleanThumbnailCache
# from core.logger import logger



# def cleanAll():
#     logger.info("Complete file cleaning is been starting")

#     CleanaptCheck()
#     cleanThumbnailCache()
#     cleanThrash()
#     cleanBrowserCache()

#     logger.info("the task succesfully done")
#     return True

import time

from Scanner.scan_engine import scanAll

from cleaner.AptCleaner import CleanaptCheck
from cleaner.Thumbnailcleaner import cleanThumbnailCache
from cleaner.BrowserClean import cleanBrowserCache
from cleaner.ThrashCleaner import cleanThrash

from ui.Finalreport import showFinalreport
from core.Errorrecover import recoverymanager
import core.report as reportData


def cleanAll():

    beforeResults = scanAll()

    totalBefore = 0

    for category in beforeResults:

        totalBefore += category.size

    reportData.beforeScanSize = totalBefore

    reportData.startTime = time.time()

    cleanThumbnailCache()

    cleanBrowserCache()

    cleanThrash()

    CleanaptCheck()

    reportData.endTime = time.time()

    afterResults = scanAll()

    totalAfter = 0

    for category in afterResults:

        totalAfter += category.size

    reportData.afterScanSize = totalAfter

    showFinalreport()
    recoverymanager.TotalsummaryReport()

    return True

