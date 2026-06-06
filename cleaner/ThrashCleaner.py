import os 
from cleaner.SafeCleaner import DeleteFile,DeleteFolder
from core.logger import logger


def cleanThrash():
    trashpath=os.path.expanduser(
         "~/.local/share/Trash/files"
    )
    logger.info("Trash Part start cleaning")
    if not os.path.exists(trashpath):
        logger.warning("Trash path not found")
        print("the thrash is been not founded")
        return False
    deletecount=0
    try:
        for item in os.listdir(trashpath):
            itemPath=os.path.join(
                trashpath,
                item
            )
            if os.path.isdir(itemPath):
                if DeleteFolder(itemPath):
                    deletecount+=1
            else:
                if DeleteFile(itemPath):
                    deletecount+=1
        logger.info(f"Deleted {deletecount} trash deleter")
        print(f"The total trash deleter{deletecount}")
        return True
    except Exception as e:
        logger.error(f"the cleaning is failed {e}")
        return False
