"""
Controlled pytest tests for cleaner.BrowserClean.cleanBrowserCache().

Replaces the old tests/BrowserCache.py, which imported and called
cleanBrowserCache() directly against the real BrowserCachePaths from
core/constants.py - i.e. the user's actual ~/.cache/google-chrome,
~/.cache/microsoft-edge, ~/.cache/chromium, ~/.cache/BraveSoftware and
~/.cache/mozilla, with zero isolation.

Every test here monkeypatches cleaner.BrowserClean.BrowserCachePaths to
point at tmp_path directories, and monkeypatches
cleaner.SafeCleaner.Expanded_SafePaths so only those tmp directories are
approved for deletion. No real browser cache directory is ever read from or
written to.
"""

import os
import stat

import cleaner.BrowserClean as BrowserClean
import cleaner.SafeCleaner as SafeCleaner


def _approve(monkeypatch, *paths):
    monkeypatch.setattr(
        SafeCleaner,
        "Expanded_SafePaths",
        [os.path.realpath(str(p)) for p in paths],
    )


def test_existing_cache_dir_is_cleaned(tmp_path, monkeypatch):
    chrome_dir = tmp_path / "chrome"
    chrome_dir.mkdir()
    (chrome_dir / "cache_file.tmp").write_text("data")

    monkeypatch.setattr(
        BrowserClean, "BrowserCachePaths", {"Chrome": str(chrome_dir)}
    )
    _approve(monkeypatch, tmp_path)

    assert BrowserClean.cleanBrowserCache() is True
    assert list(chrome_dir.iterdir()) == []


def test_missing_browser_cache_is_skipped_without_crash(tmp_path, monkeypatch):
    missing_dir = tmp_path / "does_not_exist"

    monkeypatch.setattr(
        BrowserClean, "BrowserCachePaths", {"Ghost Browser": str(missing_dir)}
    )
    _approve(monkeypatch, tmp_path)

    # Must not raise, and must still report overall success.
    assert BrowserClean.cleanBrowserCache() is True
    assert not missing_dir.exists()


def test_multiple_browsers_are_all_processed(tmp_path, monkeypatch):
    chrome_dir = tmp_path / "chrome"
    chrome_dir.mkdir()
    (chrome_dir / "a.tmp").write_text("data")

    firefox_dir = tmp_path / "firefox"
    firefox_dir.mkdir()
    (firefox_dir / "b.tmp").write_text("data")
    (firefox_dir / "subcache").mkdir()

    monkeypatch.setattr(
        BrowserClean,
        "BrowserCachePaths",
        {"Chrome": str(chrome_dir), "Firefox": str(firefox_dir)},
    )
    _approve(monkeypatch, tmp_path)

    assert BrowserClean.cleanBrowserCache() is True
    assert list(chrome_dir.iterdir()) == []
    assert list(firefox_dir.iterdir()) == []


def test_one_browser_failure_does_not_stop_another(tmp_path, monkeypatch):
    if os.geteuid() == 0:
        # root bypasses directory permission bits, so the induced listdir
        # failure below wouldn't occur - skip this case when run as root.
        return

    broken_dir = tmp_path / "broken_browser"
    broken_dir.mkdir()
    (broken_dir / "unreachable.tmp").write_text("data")

    healthy_dir = tmp_path / "healthy_browser"
    healthy_dir.mkdir()
    (healthy_dir / "cleanme.tmp").write_text("data")

    monkeypatch.setattr(
        BrowserClean,
        "BrowserCachePaths",
        {"Broken": str(broken_dir), "Healthy": str(healthy_dir)},
    )
    _approve(monkeypatch, tmp_path)

    original_mode = broken_dir.stat().st_mode
    broken_dir.chmod(0)  # no read/execute -> os.listdir() raises PermissionError

    try:
        # cleanBrowserCache's outer try/except must swallow the listdir
        # failure for "Broken" and keep going to "Healthy".
        assert BrowserClean.cleanBrowserCache() is True
        assert list(healthy_dir.iterdir()) == []
    finally:
        broken_dir.chmod(original_mode)


def test_file_and_directory_deletion_use_safe_cleaner(tmp_path, monkeypatch):
    """Verify real disappearance of both a file and a nested directory, i.e.
    that SafeCleaner is genuinely the deletion mechanism - not just that
    cleanBrowserCache() returns True."""

    browser_dir = tmp_path / "browser"
    browser_dir.mkdir()
    file_item = browser_dir / "file.tmp"
    file_item.write_text("data")
    dir_item = browser_dir / "subdir"
    dir_item.mkdir()
    (dir_item / "nested.tmp").write_text("data")

    monkeypatch.setattr(
        BrowserClean, "BrowserCachePaths", {"Chrome": str(browser_dir)}
    )
    _approve(monkeypatch, tmp_path)

    BrowserClean.cleanBrowserCache()

    assert not file_item.exists()
    assert not dir_item.exists()


def test_deletion_is_blocked_when_path_not_approved(tmp_path, monkeypatch):
    """If Expanded_SafePaths does not cover the browser cache dir,
    SafeCleaner must refuse to delete anything inside it, even though
    cleanBrowserCache() itself still reports True."""

    browser_dir = tmp_path / "browser"
    browser_dir.mkdir()
    file_item = browser_dir / "file.tmp"
    file_item.write_text("data")

    monkeypatch.setattr(
        BrowserClean, "BrowserCachePaths", {"Chrome": str(browser_dir)}
    )
    # Approve some unrelated directory only.
    other = tmp_path / "unrelated"
    other.mkdir()
    _approve(monkeypatch, other)

    BrowserClean.cleanBrowserCache()

    assert file_item.exists()
