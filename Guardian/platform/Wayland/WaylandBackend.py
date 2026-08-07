"""Wayland backend helpers for GNOME Shell communication."""
from Guardian.platform.Wayland.DBusClient import DbusClient

class WaylandBackend:
    def __init__(self):
        self.client = DbusClient()

    def isAvail(self) -> bool:
        return self.client.isAvailable()

    def getShellVersion(self):
        return self.client.shellVersion

    def backendInfo(self):
        return {
            "backend": "wayland",
            "available": self.isAvail(),
            "shellVersion": self.getShellVersion(),
        }

    def initialize(self):
        if not self.isAvail():
            raise RuntimeError("Wayland backend unavailable")
        return True
