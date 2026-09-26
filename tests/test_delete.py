"""
Controlled pytest tests for cleaner.SafeCleaner.DeleteFile / DeleteFolder.

This file previously ran DeleteFolder("/etc/passwd") as top-level module code
(executed as a side effect of pytest even importing the file, with zero
def test_...() functions to actually assert anything). It relied entirely on
SafeCleaner blocking the path to avoid disaster, and touched a real system
file path directly. It is rewritten here as real pytest tests that:

  - never reference a real system path (no /etc/passwd, no real ~/.cache),
  - use a tmp_path (pytest's tempfile-based fixture) for all filesystem data,
  - monkeypatch cleaner.SafeCleaner.Expanded_SafePaths (the name as bound
    inside SafeCleaner at import time - patching core.constants after the
    fact would not affect it) instead of touching core/constants.py.
"""

import os
import stat

import cleaner.SafeCleaner as SafeCleaner
from cleaner.SafeCleaner import DeleteFile, DeleteFolder


def _approve(monkeypatch, *paths):
    """Approve exactly the given paths as safe-delete roots for this test."""
    monkeypatch.setattr(
        SafeCleaner,
        "Expanded_SafePaths",
        [os.path.realpath(p) for p in paths],
    )


def test_delete_file_in_approved_path_succeeds(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    target = tmp_path / "approved.tmp"
    target.write_text("data")

    assert DeleteFile(str(target)) is True
    assert not target.exists()


def test_delete_folder_in_approved_path_succeeds(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    target = tmp_path / "approved_dir"
    target.mkdir()
    (target / "child.txt").write_text("data")

    assert DeleteFolder(str(target)) is True
    assert not target.exists()


def test_delete_file_outside_approved_path_is_rejected(tmp_path, monkeypatch):
    approved = tmp_path / "approved"
    approved.mkdir()
    _approve(monkeypatch, approved)

    unapproved_dir = tmp_path / "unapproved"
    unapproved_dir.mkdir()
    target = unapproved_dir / "file.tmp"
    target.write_text("data")

    assert DeleteFile(str(target)) is False
    assert target.exists()


def test_delete_folder_outside_approved_path_is_rejected(tmp_path, monkeypatch):
    approved = tmp_path / "approved"
    approved.mkdir()
    _approve(monkeypatch, approved)

    unapproved = tmp_path / "unapproved_dir"
    unapproved.mkdir()

    assert DeleteFolder(str(unapproved)) is False
    assert unapproved.exists()


def test_delete_symlink_target_is_rejected(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    real_file = tmp_path / "real.txt"
    real_file.write_text("data")

    link = tmp_path / "link.txt"
    link.symlink_to(real_file)

    # The symlink itself lives inside an approved path, but SafeCleaner must
    # still refuse to act on it - symlinks are never deleted.
    assert DeleteFile(str(link)) is False
    assert link.exists()
    assert real_file.exists()


def test_delete_symlink_folder_is_rejected(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    real_dir = tmp_path / "real_dir"
    real_dir.mkdir()

    link_dir = tmp_path / "link_dir"
    link_dir.symlink_to(real_dir, target_is_directory=True)

    assert DeleteFolder(str(link_dir)) is False
    assert link_dir.exists()
    assert real_dir.exists()


def test_delete_nonexistent_file_returns_false(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    missing = tmp_path / "does_not_exist.tmp"

    assert DeleteFile(str(missing)) is False


def test_delete_nonexistent_folder_returns_false(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    missing = tmp_path / "no_such_dir"

    assert DeleteFolder(str(missing)) is False


def test_delete_file_permission_denied_returns_false(tmp_path, monkeypatch):
    """A file inside an approved directory whose parent dir forbids writes
    cannot be unlinked - DeleteFile must catch PermissionError and return
    False rather than raising."""

    if os.geteuid() == 0:
        # root can delete regardless of directory permission bits - this
        # case can't be exercised meaningfully when running as root.
        return

    locked_dir = tmp_path / "locked"
    locked_dir.mkdir()
    target = locked_dir / "file.tmp"
    target.write_text("data")

    _approve(monkeypatch, tmp_path)

    original_mode = locked_dir.stat().st_mode
    locked_dir.chmod(stat.S_IREAD | stat.S_IEXEC)  # r-x, no write

    try:
        assert DeleteFile(str(target)) is False
        assert target.exists()
    finally:
        locked_dir.chmod(original_mode)
