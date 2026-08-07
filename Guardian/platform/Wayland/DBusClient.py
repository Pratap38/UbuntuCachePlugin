import subprocess

class DbusClient:
    def __init__(self):
        self.available = False
        self.shellVersion = None
        self.initialize()

    def initialize(self):
        """Initialize the D-Bus connection."""
        try:
            result = subprocess.run(
                [
                    "gdbus",
                    "call",
                    "--session",
                    "--dest",
                    "org.gnome.Shell",
                    "--object-path",
                    "/org/gnome/Shell",
                    "--method",
                    "org.freedesktop.DBus.Peer.Ping",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.available = result.returncode == 0

            if self.available:
                self.shellVersion = self.getShellVersion()

        except Exception:
            self.available = False

    def isAvailable(self) -> bool:
        return self.available

    def getShellVersion(self):
        try:
            result = subprocess.run(
                [
                    "gdbus",
                    "call",
                    "--session",
                    "--dest",
                    "org.gnome.Shell",
                    "--object-path",
                    "/org/gnome/Shell",
                    "--method",
                    "org.freedesktop.DBus.Properties.Get",
                    "org.gnome.Shell",
                    "ShellVersion",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                return result.stdout.strip()

        except Exception:
            pass

        return None

    def info(self):
        """Return backend information."""
        return {
            "available": self.available,
            "shell_version": self.shellVersion,
        }
