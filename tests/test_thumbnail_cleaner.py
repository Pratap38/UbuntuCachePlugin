"""
Controlled pytest tests for cleaner.Thumbnailcleaner.cleanThumbnailCache().

Replaces tests/testthumbnail.py, which called cleanThumbnailCache() directly
against the real ~/.cache/thumbnails with zero isolation.

cleanThumbnailCache() hardcodes the path via
os.path.expanduser("~/.cache/thumbnails") inline (there is no module-level
constant to monkeypatch). To redirect it without touching production code,
these tests monkeypatch os.path.expanduser itself with a wrapper that only
intercepts that one literal string and redirects it to a tmp_path directory;
every other call (e.g. inside SafeCleaner) falls through to the real
os.path.expanduser unchanged. The real ~/.cache/thumbnails is never read
from or written to by these tests.
"""

import os

import cleaner.SafeCleaner as SafeCleaner
from cleaner.Thumbnailcleaner import cleanThumbnailCache

REAL_TARGET = "~/.cache/thumbnails"


def _redirect_thumbnail_path(monkeypatch, tmp_path):
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


def test_existing_thumbnail_cache_is_cleaned(tmp_path, monkeypatch):
    cache_dir = tmp_path / "thumbnails"
    cache_dir.mkdir()
    _redirect_thumbnail_path(monkeypatch, cache_dir)

    (cache_dir / "thumb1.png").write_text("data")
    sub = cache_dir / "large"
    sub.mkdir()
    (sub / "thumb2.png").write_text("data")

    assert cleanThumbnailCache() is True
    assert list(cache_dir.iterdir()) == []


def test_missing_thumbnail_cache_is_skipped_without_crash(tmp_path, monkeypatch):
    missing = tmp_path / "no_thumbnails_here"
    _redirect_thumbnail_path(monkeypatch, missing)

    assert cleanThumbnailCache() is False
    assert not missing.exists()
