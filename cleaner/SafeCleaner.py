import os
import shutil

from ui.Deleteui import showDeleting
from core.logger import logger
from core.constants import Expanded_SafePaths
from core.Errorrecover import recoverymanager


def isSafePaths(path):

    expandPath = os.path.abspath(
        os.path.expanduser(path)
    )

    for safePath in Expanded_SafePaths:

        if expandPath.startswith(safePath):

            return True

    return False


def isSymlink(path):

    return os.path.islink(path)


#for deleting file
def DeleteFile(path):

    try:

        if not os.path.exists(path):

            logger.warning(
                f"file Not found:{path}"
            )

            return False

        if isSymlink(path):

            logger.warning(
                f"Skipped symlink: {path}"
            )

            return False

        if not isSafePaths(path):

            recoverymanager.addFailedfile(path)

            logger.error(
                f"unsafe file delete blocked:{path}"
            )

            return False

        showDeleting(path)

        os.remove(path)

        logger.info(
            f"file Delete Succesfull:{path}"
        )

        return True

    except PermissionError:

        recoverymanager.addPermissionerror(
            path
        )

        logger.error(
            f"Permission Denied /failed {path}"
        )

        return False

    except Exception as e:

        recoverymanager.addFailedfile(
            path
        )

        logger.error(
            f"failed delete file {path}:{e}"
        )

        return False


#for deleting Folder
def DeleteFolder(path):

    try:

        if not os.path.exists(path):

            logger.warning(
                f"Folder not found: {path}"
            )

            return False

        if isSymlink(path):

            logger.warning(
                f"Skipped symlink folder: {path}"
            )

            return False

        if not isSafePaths(path):

            recoverymanager.addFailedfile(
                path
            )

            logger.error(
                f"Unsafe folder delete blocked: {path}"
            )

            return False

        showDeleting(path)

        shutil.rmtree(path)

        logger.info(
            f"Deleted folder: {path}"
        )

        return True

    except PermissionError:

        recoverymanager.addPermissionerror(
            path
        )

        logger.error(
            f"Permission Denied/Failed {path}"
        )

        return False

    except Exception as e:

        recoverymanager.addFailedfile(
            path
        )

        logger.error(
            f"Failed deleting folder {path}: {e}"
        )

        return False