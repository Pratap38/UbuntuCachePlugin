import signal

from Guardian.GuardianEngine import GuardianEngine



##we will use this command first in order to stop SIGTERM → normal systemd stop
# SIGINT  → Ctrl+C / manual interruption
def main():

    engine=GuardianEngine()

    def handleShutdown(signum,frame):
        engine.stop()
    signal.signal(signal.SIGTERM,handleShutdown)
    signal.signal(signal.SIGINT,handleShutdown)

    engine.start()

if __name__ == "__main__":
    main()