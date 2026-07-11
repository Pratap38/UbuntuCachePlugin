import os
import shutil
import platform


class EnvironmentChecker:

    def __init__(self):

        self.warnings = []

    def check(self):

        self.checkUbuntu()

        self.checkAPT()

        self.checkHome()

        return self.warnings

    def checkUbuntu(self):

        if platform.system() != "Linux":

            self.warnings.append(

                "Running on unsupported operating system."

            )

    def checkAPT(self):

        if shutil.which("apt") is None:

            self.warnings.append(

                "APT package manager not found."

            )

    def checkHome(self):

        if not os.path.exists(

            os.path.expanduser("~")

        ):

            self.warnings.append(

                "Home directory not found."

            )