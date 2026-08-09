import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from Guardian.Focus.FocusTrackerWayland import FocusTrackerWayland
from Guardian.platform.Wayland.FocusReceiver import FocusReceiver


class TestFocusReceiver(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.socket_path = os.path.join(self.tmpdir.name, "ram-guardian-focus.sock")

    def tearDown(self):
        self.tmpdir.cleanup()

    @patch("Guardian.platform.Wayland.FocusReceiver.os.unlink")
    @patch("Guardian.platform.Wayland.FocusReceiver.os.remove")
    @patch("Guardian.platform.Wayland.FocusReceiver.os.path.exists")
    @patch("Guardian.platform.Wayland.FocusReceiver.stat_is_socket")
    @patch("Guardian.platform.Wayland.FocusReceiver.socket.socket")
    @patch("Guardian.platform.Wayland.FocusReceiver.os.chmod")
    def test_socket_creation_and_shutdown(
        self,
        mock_chmod,
        mock_socket_cls,
        mock_stat_is_socket,
        mock_exists,
        mock_remove,
        mock_unlink,
    ):
        mock_socket = MagicMock()
        mock_socket.accept.side_effect = OSError("stop")
        mock_socket_cls.return_value = mock_socket
        mock_exists.return_value = False
        mock_stat_is_socket.return_value = False

        receiver = FocusReceiver(self.socket_path)
        receiver.start()

        self.assertIsNotNone(receiver._server)
        mock_socket.bind.assert_called_once_with(self.socket_path)
        mock_socket.listen.assert_called_once_with(5)
        mock_chmod.assert_called_once()

        receiver.stop()

        self.assertFalse(receiver.is_running())
        mock_socket.close.assert_called()

    def test_rejects_invalid_json(self):
        receiver = FocusReceiver(self.socket_path)
        receiver._handle_line(b"{not-json}\n")
        self.assertIsNone(receiver.get_latest_window())

    def test_missing_fields_use_defaults(self):
        receiver = FocusReceiver(self.socket_path)
        receiver._handle_line(json.dumps({"pid": 42}).encode("utf-8") + b"\n")

        window = receiver.get_latest_window()

        self.assertIsNotNone(window)
        self.assertEqual(window.application, "Unknown")
        self.assertEqual(window.pid, 42)
        self.assertEqual(window.window_id, "WAYLAND")

    @patch("Guardian.platform.Wayland.FocusReceiver.os.chmod")
    @patch("Guardian.platform.Wayland.FocusReceiver.os.unlink")
    @patch("Guardian.platform.Wayland.FocusReceiver.os.path.exists")
    @patch("Guardian.platform.Wayland.FocusReceiver.stat_is_socket")
    @patch("Guardian.platform.Wayland.FocusReceiver.socket.socket")
    def test_stale_socket_cleanup(
        self,
        mock_socket_cls,
        mock_stat_is_socket,
        mock_exists,
        mock_unlink,
        mock_chmod,
    ):
        mock_exists.return_value = True
        mock_stat_is_socket.return_value = True
        mock_socket = MagicMock()
        mock_socket.accept.side_effect = OSError("stop")
        mock_socket_cls.return_value = mock_socket

        receiver = FocusReceiver(self.socket_path)
        receiver.start()

        mock_unlink.assert_called_once_with(self.socket_path)
        mock_socket.bind.assert_called_once_with(self.socket_path)
        receiver.stop()

    def test_latest_focus_state_updates(self):
        receiver = FocusReceiver(self.socket_path)
        payload = {
            "application": "Firefox",
            "app_id": "firefox.desktop",
            "pid": 12345,
            "title": "ChatGPT",
            "window_id": 999,
            "focused": True,
            "timestamp": "2026-08-08T10:11:12",
        }

        receiver._handle_line((json.dumps(payload) + "\n").encode("utf-8"))
        window = receiver.get_latest_window()

        self.assertEqual(window.application, "Firefox")
        self.assertEqual(window.pid, 12345)
        self.assertEqual(window.window_id, 999)

    def test_clean_shutdown(self):
        receiver = FocusReceiver(self.socket_path)
        server = MagicMock()
        receiver._server = server
        receiver._thread = MagicMock()
        receiver._thread.is_alive.return_value = False
        receiver._running = True

        receiver.stop()

        self.assertFalse(receiver.is_running())
        server.close.assert_called_once()


class TestFocusTrackerWaylandWithReceiver(unittest.TestCase):
    def test_tracker_uses_receiver_window(self):
        receiver = MagicMock()
        receiver.is_running.return_value = True
        receiver.get_latest_window.return_value = MagicMock(
            application="Terminal",
            pid=4350,
            window_id=3130767378,
            title="~/D/UbuntuCacheCLeaner",
            focused=True,
        )

        tracker = FocusTrackerWayland(receiver=receiver, autostart=False)
        window = tracker.getActiveWindow()

        self.assertEqual(window.application, "Terminal")
        self.assertEqual(window.pid, 4350)
        self.assertEqual(window.window_id, 3130767378)


if __name__ == "__main__":
    unittest.main()
