from Guardian.Focus.FocusTrackerBase import FocusTracker
from Guardian.models.WindowInfo import WindowInfo
from Guardian.platform.Wayland.WindowDetector import WindowDetector
from Guardian.platform.Wayland.FocusReceiver import FocusReceiver


class FocusTrackerWayland(FocusTracker):

    def __init__(self, receiver=None, autostart=True):
        

        self.detector = WindowDetector()

        
        self.receiver = receiver or FocusReceiver()

        # Start the IPC receiver automatically in normal operation.
        if autostart and not self.receiver.is_running():
            self.receiver.start()

        self.currentWindow = None


    def getActiveWindow(self) -> WindowInfo | None:
       

        receiver_window = self.receiver.get_latest_window()

        if receiver_window is not None:
            self.currentWindow = receiver_window
            return self.currentWindow

      
        return self.currentWindow

  

    def getFocusedApplication(self):
      

        window = self.getActiveWindow()

        if window is not None:
            return window.application

        return None

    
    @classmethod
    def isSupported(cls):
       

        return WindowDetector().supportDetector()

  

    def refresh(self):
       

        self.currentWindow = self.receiver.get_latest_window()

        return self.currentWindow

   

    def stop(self):
       

        if self.receiver.is_running():
            self.receiver.stop()

        self.currentWindow = None
