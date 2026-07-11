import os
from datetime import datetime


class RecoveryLogger:

    LOG_FILE = "logs/recovery.log"

    @classmethod
    def log(

        cls,

        message

    ):

        os.makedirs(

            "logs",

            exist_ok=True

        )

        with open(

            cls.LOG_FILE,

            "a"

        ) as file:

            file.write(

                f"[{datetime.now()}] "

            )

            file.write(

                message

            )

            file.write(

                "\n"

            )