import os
from cleaner.SafeCleaner import DeleteFile,DeleteFolder
from core.logger import logger
from core.constants import BrowserCachePaths

def cleanBrowserCache():
    cleanCount=0
    logger.info("Starting Browser Clean ")

    for browser,path in BrowserCachePaths.items():
        expandPath=os.path.expanduser(path)
        if not os.path.exists(expandPath):
            logger.warning(f"{browser}cache not found:")
            continue
        try:
            for item in os.listdir(expandPath):
                itemPath=os.path.join(
                    expandPath,
                    item
                )
                try:
                    if os.path.isdir(itemPath):
                        DeleteFolder(itemPath)
                    else:
                        DeleteFile(itemPath)
                except Exception as e:
                    logger.error(f"{browser}error  failed to clean item {itemPath}: {e}")
            cleanCount+=1
        except Exception as e:
            logger.error(f"{browser}error  failed to clean {e}")
    print(f"{cleanCount} number of browser cache is been ccleaned" )
    return True
            