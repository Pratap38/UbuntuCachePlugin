"""
Manual live check for the GNOME -> Python focus IPC.

Not a pytest test (no automated assertions) - this starts the real
FocusReceiver against the real socket and prints whatever arrives, so you
can confirm the GNOME extension is actually reaching Python.

Run:
    PYTHONPATH=. python Guardian/tests/live_focus_listener.py

Then switch focus between a couple of windows and watch for
"FOCUS RECEIVED" lines. Stop with Ctrl+C.
"""

import time

from Guardian.platform.Wayland.FocusReceiver import FocusReceiver


def main():
    receiver = FocusReceiver()
    receiver.start()

    print("Receiver running:", receiver.is_running())
    print("Socket:", receiver.socket_path)
    print("Waiting for focus payload...")

    try:
        while True:
            window = receiver.get_latest_window()
            if window:
                print("FOCUS RECEIVED:", window)
            time.sleep(0.5)
    except KeyboardInterrupt:
        receiver.stop()


if __name__ == "__main__":
    main()
