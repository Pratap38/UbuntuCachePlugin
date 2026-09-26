"""
Controlled pytest tests for cleaner.ThrashCleaner.cleanThrash().

Replaces tests/Thrashfile.py, which called cleanThrash() directly against
the real ~/.local/share/Trash/files with zero isolation.

cleanThrash() hardcodes the path via
os.path.expanduser("~/.local/share/Trash/files") inline. As with the
thumbnail cleaner tests, os.path.expanduser is monkeypatched to redirect
only that exact literal string to a tmp_path directory; every other call
falls through unchanged. The real Trash is never touched.
"""

import os

import cleaner.SafeCleaner as SafeCleaner
from cleaner.ThrashCleaner import cleanThrash

REAL_TARGET = "~/.local/share/Trash/files"


def _redirect_trash_path(monkeypatch, tmp_path):
    real_expanduser = os.path.expanduser

    def fake_expanduser(path):
        if path == REAL_TARGET:
            return str(tmp_path)
        return real_expanduser(path)

    monkeypatch.setattr(os.path, "expanduser", fake_expanduser)
    monkeypatch.setattr(
        SafeCleaner,
        "Expanded_SafePaths",
        [os.path.realpath(str(tmp_path))],
    )


def test_existing_trash_is_cleaned(tmp_path, monkeypatch):
    trash_dir = tmp_path / "trash"
    trash_dir.mkdir()
    _redirect_trash_path(monkeypatch, trash_dir)

    (trash_dir / "deleted_file.txt").write_text("data")
    folder = trash_dir / "deleted_folder"
    folder.mkdir()
    (folder / "inner.txt").write_text("data")

    assert cleanThrash() is True
    assert list(trash_dir.iterdir()) == []


def test_missing_trash_is_skipped_without_crash(tmp_path, monkeypatch):
    missing = tmp_path / "no_trash_here"
    _redirect_trash_path(monkeypatch, missing)

    assert cleanThrash() is False
    assert not missing.exists()
