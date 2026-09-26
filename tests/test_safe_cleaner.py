"""
Controlled pytest tests for cleaner.SafeCleaner.isSafePaths() - the real
containment check (os.path.realpath + os.path.commonpath) that replaced the
old naive string-prefix check.

All paths used here are inside tmp_path; nothing under a real user/system
path (~/.cache, /etc, /var, real Trash, ...) is ever touched.
"""

import os

import cleaner.SafeCleaner as SafeCleaner
from cleaner.SafeCleaner import DeleteFile, isSafePaths


def _approve(monkeypatch, *paths):
    monkeypatch.setattr(
        SafeCleaner,
        "Expanded_SafePaths",
        [os.path.realpath(p) for p in paths],
    )


def test_allowed_path_is_approved(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    target = tmp_path / "file.tmp"
    target.write_text("x")

    assert isSafePaths(str(target)) is True


def test_nested_allowed_path_is_approved(tmp_path, monkeypatch):
    _approve(monkeypatch, tmp_path)

    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    target = nested / "deep.tmp"
    target.write_text("x")

    assert isSafePaths(str(target)) is True


def test_sibling_prefix_is_rejected(tmp_path, monkeypatch):
    """Mirrors the class of bug just fixed: an approved dir named "foo" must
    not also approve a sibling directory named "foo-other" just because the
    string "foo" is a prefix of "foo-other"."""

    approved = tmp_path / "foo"
    approved.mkdir()
    sibling = tmp_path / "foo-other"
    sibling.mkdir()

    _approve(monkeypatch, approved)

    target = sibling / "file.tmp"
    target.write_text("x")

    assert isSafePaths(str(target)) is False
    # Confirm end-to-end that DeleteFile also refuses it.
    assert DeleteFile(str(target)) is False
    assert target.exists()


def test_unrelated_path_is_rejected(tmp_path, monkeypatch):
    approved = tmp_path / "approved"
    approved.mkdir()
    unrelated = tmp_path / "elsewhere"
    unrelated.mkdir()

    _approve(monkeypatch, approved)

    target = unrelated / "file.tmp"
    target.write_text("x")

    assert isSafePaths(str(target)) is False


def test_approved_path_itself_is_approved(tmp_path, monkeypatch):
    """The approved root path itself (not just its children) should also be
    considered safe by the containment check."""

    approved = tmp_path / "approved"
    approved.mkdir()

    _approve(monkeypatch, approved)

    assert isSafePaths(str(approved)) is True
