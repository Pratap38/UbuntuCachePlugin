import json
import os
import socket
import stat
import threading
from pathlib import Path

from Guardian.platform.Wayland.FocusPayload import (
    normalize_focus_payload,
    window_info_from_focus_payload,
)


class FocusReceiver:
    def __init__(self, socket_path: str | None = None):
        self.socket_path = socket_path or self._default_socket_path()
        self._server = None
        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._latest_window = None
        self._running = False

    def _default_socket_path(self) -> str:
        runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        if runtime_dir:
            return str(Path(runtime_dir) / "ram-guardian-focus.sock")
        return f"/run/user/{os.getuid()}/ram-guardian-focus.sock"

    def _cleanup_stale_socket(self) -> None:
        try:
            if os.path.exists(self.socket_path):
                if stat_is_socket(self.socket_path):
                    os.unlink(self.socket_path)
                else:
                    os.remove(self.socket_path)
        except FileNotFoundError:
            pass

    def start(self) -> None:
        if self._running:
            return

        self._cleanup_stale_socket()
        self._server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server.bind(self.socket_path)
        self._server.listen(5)
        os.chmod(self.socket_path, 0o600)
        self._stop_event.clear()
        self._running = True
        self._thread = threading.Thread(
            target=self._serve,
            name="RamGuardianFocusReceiver",
            daemon=True,
        )
        self._thread.start()

    def _serve(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._server.settimeout(0.5)
                accepted = self._server.accept()
                conn = accepted[0] if isinstance(accepted, tuple) else accepted
            except socket.timeout:
                continue
            except OSError:
                break

            with conn:
                buffer = b""
                while not self._stop_event.is_set():
                    try:
                        chunk = conn.recv(4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        self._handle_line(line)

        self._running = False

    def _handle_line(self, line: bytes) -> None:
        text = line.decode("utf-8", errors="replace").strip()
        if not text:
            return

        try:
            payload = json.loads(text)
            if not isinstance(payload, dict):
                return

            normalized = normalize_focus_payload(payload)
            window = window_info_from_focus_payload(normalized)

        except (json.JSONDecodeError, TypeError, ValueError):
            return

        with self._lock:
            self._latest_window = window

    def stop(self) -> None:
        self._stop_event.set()
        self._running = False

        if self._server is not None:
            try:
                self._server.close()
            finally:
                self._server = None

        try:
            if os.path.exists(self.socket_path):
                os.unlink(self.socket_path)
        except FileNotFoundError:
            pass

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

        self._thread = None

    def get_latest_window(self):
        with self._lock:
            return self._latest_window

    def is_running(self) -> bool:
        return self._running


def stat_is_socket(path: str) -> bool:
    try:
        return stat.S_ISSOCK(os.stat(path).st_mode)
    except Exception:
        return False
