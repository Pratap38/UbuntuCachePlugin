from pathlib import Path
from datetime import datetime

class GuardLogManager:
    def __init__(self):

        self.logDirectory = (

            Path(__file__).parent

            / "logs"

        )

        self.logFile = (

            self.logDirectory

            / "guardian.log"

        )

        self.logDirectory.mkdir(

            exist_ok=True

        )

        self.logFile.touch(
            exist_ok=True
        )

    def log(

        self,

        level,

        message

    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        entry = (
            f"[{timestamp}] "
            f"[{level}] "
            f"{message}\n"
        )

        with open(
            self.logFile,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                entry
            )

    def info(

        self,

        message

    ):

        self.log(

            "INFO",

            message
        )

    def warning(

        self,
        message
    ):

        self.log(
            "WARNING",
            message
        )

    # -----------------------------------------------------

    def error(

        self,

        message

    ):

        self.log(

            "ERROR",

            message

        )

    # -----------------------------------------------------

    def critical(

        self,

        message

    ):

        self.log(

            "CRITICAL",

            message

        )

    # -----------------------------------------------------

    def clear(self):

        with open(
            self.logFile,
            "w",
            encoding="utf-8"
        ):
            pass

    # -----------------------------------------------------

    def read(self):

        with open(
            self.logFile,
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    # -----------------------------------------------------

    def exists(self):

        return self.logFile.exists()

    # -----------------------------------------------------

    def path(self):

        return str(
            self.logFile
        )
