import os
import time

from cleaner.SafeCleaner import DeleteFile
from core.logger import logger

TEMP_PATH = "/tmp"
MIN_FILE_AGE = 60 * 60  

def cleanTempFiles():
    deleted=0
    failed=0
    skipped=0

    try:
        now=time.time()
        for name in os.listdir(TEMP_PATH):
            path=os.path.join(TEMP_PATH,name)
            try:
                if os.path.islink(path):
                    skipped+=1
                    logger.info(f"skipped link:{path}")
                    continue

                if not os.path.isfile(path):
                    skipped+=1
                    continue
                age=now-os.path.getmtime(path)

                if age<MIN_FILE_AGE:
                    skipped+=1
                    logger.info(f"total skipped temp file recent: {path}")
                    continue
                if DeleteFile(path):
                    deleted+=1
                else:
                    failed+=1

            except (FileNotFoundError, PermissionError, OSError) as e:
                        failed += 1
                        logger.warning(
                            f"Could not process temp file {path}: {e}"
                        )
        logger.info(
                f"Temp Files cleanup completed: "
                f"{deleted} deleted, {failed} failed, {skipped} skipped."
            )

        return failed == 0

    except Exception as e:
        logger.error(f"Temp Files cleanup failed: {e}")
        return False