"""
Controlled pytest tests for cleaner.TempCleaner.cleanTempFiles().

cleanTempFiles() hardcodes TEMP_PATH = "/tmp" at module scope. Rather than
letting it operate on the real /tmp, every test here monkeypatches
cleaner.TempCleaner.TEMP_PATH to point at a tmp_path fixture directory, and
monkeypatches cleaner.SafeCleaner.Expanded_SafePaths so that directory (and
only that directory) is approved for the duration of the test. Real /tmp
contents are never touched.
"""

import os
import stat
import time

import cleaner.SafeCleaner as SafeCleaner
import cleaner.TempCleaner as TempCleaner


def _prepare(monkeypatch, tmp_path):
    monkeypatch.setattr(TempCleaner, "TEMP_PATH", str(tmp_path))
    monkeypatch.setattr(
        SafeCleaner,
        "Expanded_SafePaths",
        [os.path.realpath(str(tmp_path))],
    )


def _make_old_file(path, age_seconds=2 * 60 * 60):
    path.write_text("old data")
    old_time = time.time() - age_seconds
    os.utime(str(path), (old_time, old_time))


def test_old_file_is_deleted(tmp_path, monkeypatch):
    _prepare(monkeypatch, tmp_path)

    old_file = tmp_path / "old.tmp"
    _make_old_file(old_file)

    assert TempCleaner.cleanTempFiles() is True
    assert not old_file.exists()


def test_recent_file_is_preserved(tmp_path, monkeypatch):
    _prepare(monkeypatch, tmp_path)

    recent_file = tmp_path / "recent.tmp"
    recent_file.write_text("fresh data")  # mtime = now

    assert TempCleaner.cleanTempFiles() is True
    assert recent_file.exists()


def test_directory_is_preserved(tmp_path, monkeypatch):
    _prepare(monkeypatch, tmp_path)

    old_dir = tmp_path / "old_dir"
    old_dir.mkdir()
    old_time = time.time() - 2 * 60 * 60
    os.utime(str(old_dir), (old_time, old_time))

    assert TempCleaner.cleanTempFiles() is True
    assert old_dir.exists()


def test_symlink_is_preserved(tmp_path, monkeypatch):
    _prepare(monkeypatch, tmp_path)

    real_target = tmp_path / "target.tmp"
    real_target.write_text("data")

    link = tmp_path / "link.tmp"
    link.symlink_to(real_target)
    # Backdate the symlink's own mtime (lstat-based) where possible; even if
    # not, cleanTempFiles must skip it purely because it's a symlink.
    old_time = time.time() - 2 * 60 * 60
    try:
        os.utime(str(link), (old_time, old_time), follow_symlinks=False)
    except (NotImplementedError, OSError):
        pass

    assert TempCleaner.cleanTempFiles() is True
    assert link.exists() or link.is_symlink()
    assert real_target.exists()


def test_permission_failure_is_reported_without_crash(tmp_path, monkeypatch):
    if os.geteuid() == 0:
        return

    _prepare(monkeypatch, tmp_path)

    old_file = tmp_path / "locked_old.tmp"
    _make_old_file(old_file)

    original_mode = tmp_path.stat().st_mode
    tmp_path.chmod(stat.S_IREAD | stat.S_IEXEC)  # remove write on the dir

    try:
        result = TempCleaner.cleanTempFiles()
        assert result is False
        assert old_file.exists()
    finally:
        tmp_path.chmod(original_mode)


def test_return_value_reflects_success_and_failure(tmp_path, monkeypatch):
    _prepare(monkeypatch, tmp_path)

    old_file = tmp_path / "old.tmp"
    _make_old_file(old_file)
    recent_file = tmp_path / "recent.tmp"
    recent_file.write_text("data")

    assert TempCleaner.cleanTempFiles() is True
    assert not old_file.exists()
    assert recent_file.exists()
