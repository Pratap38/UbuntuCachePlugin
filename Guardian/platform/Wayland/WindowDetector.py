##Active window detail

from Guardian.platform.Wayland.WaylandBackend import  WaylandBackend

class WindowDetector:
    def __init__(self):
         self.backend=WaylandBackend()

    def isAvail(self) -> bool:
                 return self.backend.isAvailable()
    def supportDetector(self)->bool:
           return self.isAvail()
    def detect():
           return None
    def info(self):
            return {

            "backend": "Wayland",

            "available": self.isAvail(),

            "supports_detection":

                self.supportDetector()

        }