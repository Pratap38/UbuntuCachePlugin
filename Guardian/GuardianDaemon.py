# import signal

# from Guardian.GuardianEngine import GuardianEngine



# ##we will use this command first in order to stop SIGTERM → normal systemd stop
# # SIGINT  → Ctrl+C / manual interruption
# def main():

#     engine=GuardianEngine()

#     def handleShutdown(signum,frame):
#         engine.stop()
#     signal.signal(signal.SIGTERM,handleShutdown)
#     signal.signal(signal.SIGINT,handleShutdown)

#     engine.start()

# if __name__ == "__main__":
#     main()



import fcntl
import signal

from Guardian.GuardianEngine import GuardianEngine
from Guardian.GuardianPaths import GuardianPaths


def main():

    lockFile = GuardianPaths.stateDirectory() / "guardian.lock"

    lockFile.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    lockHandle = open(
        lockFile,
        "w",
        encoding="utf-8"
    )

    try:

        try:

            fcntl.flock(
                lockHandle.fileno(),
                fcntl.LOCK_EX | fcntl.LOCK_NB
            )

        except BlockingIOError:

            print(
                "RAM Guardian is already running."
            )

            return

        engine = GuardianEngine()

        def handleShutdown(signum, frame):
            engine.stop()

        signal.signal(
            signal.SIGTERM,
            handleShutdown
        )

        signal.signal(
            signal.SIGINT,
            handleShutdown
        )

        engine.start()

    finally:

        try:

            fcntl.flock(
                lockHandle.fileno(),
                fcntl.LOCK_UN
            )

        finally:

            lockHandle.close()


if __name__ == "__main__":
    main()