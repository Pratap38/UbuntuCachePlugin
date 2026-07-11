import os
import traceback
from datetime import datetime


class CrashLogger:

    LOG_FILE = "logs/crash.log"

    @classmethod
    def log(cls, exception):

        os.makedirs(

            "logs",

            exist_ok=True

        )

        with open(

            cls.LOG_FILE,

            "a"

        ) as file:

            file.write(

                "\n"

            )

            file.write(

                "=" * 60

            )

            file.write(

                "\n"

            )

            file.write(

                str(

                    datetime.now()

                )

            )

            file.write(

                "\n\n"

            )

            file.write(

                traceback.format_exc()

            )