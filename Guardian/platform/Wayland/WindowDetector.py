##Active window detail
import subprocess

from Guardian.platform.Wayland.WaylandBackend import  WaylandBackend

class WindowDetector:
    def __init__(self):
         self.backend=WaylandBackend()

    def isAvail(self) -> bool:
                 return self.backend.isAvailable()
    def supportDetector(self)->bool:
           if not self.isAvail():

            return False

           try:

                result = subprocess.run(

                    [

                        "gdbus",

                        "introspect",

                        "--session",

                        "--dest",

                        "org.gnome.Shell",

                        "--object-path",

                        "/org/gnome/Shell/Introspect"

                    ],

                    capture_output=True,

                    text=True,

                    timeout=5

                )

                return result.returncode == 0

           except Exception:

                return False
    def detect(self):
          if not self.supportDetector():

            return None

          return {

                "interface":

                    "org.gnome.Shell.Introspect",

                "status":

                    "available"

            }
    def info(self):
            return {

            "backend": "Wayland",

            "available": self.isAvail(),

            "supports_detection":

                self.supportDetector()

        }