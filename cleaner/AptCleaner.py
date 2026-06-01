import subprocess  ##python module to run the external linux command

from core.logger import logger
from core.permission import isRootUser


def CleanaptCheck():
    if not isRootUser():
        print("Apt cleaning require root users")
        logger.warning("Api clean attmpet without sudo root user")

        return False
    try:
        logger.info("starting APT file cleaning ***")
        result=subprocess.run(
            ["apt","clean"],
            capture_output=True,
            text=True

        )
        if result.returncode==0:
            logger.info("Apt clean successfull")
            print("Apt clean success")
            return True
        else:
            logger.error(f"apt failed {result.stderr}")
            print("APt clean Falied")
    except Exception as e:
        logger.error(f"apte crahsed {e}")
        return False