import json
import unittest
from pathlib import Path

from Guardian.platform.Wayland.FocusPayload import (
    normalize_focus_payload,
    window_info_from_focus_payload,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
EXT_DIR = REPO_ROOT / "gnome-extension" / "ram-guardian-focus"


class TestGnomeExtensionIntegration(unittest.TestCase):
    def test_metadata_is_valid_for_gnome_46(self):
        metadata = json.loads((EXT_DIR / "metadata.json").read_text())
        self.assertEqual(metadata["uuid"], "ram-guardian-focus@ubuntu-cache-cleaner")
        self.assertIn("46", metadata["shell-version"])

    def test_extension_payload_normalization(self):
        payload = {
            "application": "Firefox",
            "app_id": "firefox.desktop",
            "pid": 12345,
            "title": "ChatGPT - Mozilla Firefox",
            "window_id": "0x1234",
            "focused": True,
            "timestamp": "2026-08-08T10:11:12",
        }

        normalized = normalize_focus_payload(payload)

        self.assertEqual(normalized["application"], "Firefox")
        self.assertEqual(normalized["app_id"], "firefox.desktop")
        self.assertEqual(normalized["pid"], 12345)
        self.assertEqual(normalized["window_id"], "0x1234")

    def test_window_info_creation_from_focus_payload(self):
        payload = {
            "application": "Terminal",
            "app_id": "org.gnome.Terminal.desktop",
            "pid": 23456,
            "title": "bash",
            "window_id": "0x5678",
            "focused": True,
            "timestamp": "2026-08-08T10:11:12",
        }

        window = window_info_from_focus_payload(payload)

        self.assertEqual(window.application, "Terminal")
        self.assertEqual(window.pid, 23456)
        self.assertEqual(window.window_id, "0x5678")
        self.assertTrue(window.focused)


if __name__ == "__main__":
    unittest.main()
