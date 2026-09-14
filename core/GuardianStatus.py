import subprocess
from pathlib import Path


class GuardianStatus:

    SERVICE_NAME = "ubuntu-cache-cleaner-guardian.service"

    def unitFilePath(self) -> Path:

        return (
            Path.home()
            / ".config"
            / "systemd"
            / "user"
            / self.SERVICE_NAME
        )

    def check(self) -> str:

        if not self.unitFilePath().exists():

            return "Not installed"

        try:

            result = subprocess.run(
                [
                    "systemctl",
                    "--user",
                    "is-active",
                    self.SERVICE_NAME
                ],
                capture_output=True,
                text=True,
                timeout=3
            )

            if result.stdout.strip() == "active":

                return "Running"

            return "Stopped"

        except Exception:

            return "Stopped"
