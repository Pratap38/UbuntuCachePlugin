"""
Controlled pytest tests for cleaner.CleanerEngine.cleanSelectedCache().

These tests never invoke the real underlying cleaners (which would touch
real ~/.cache, real browser caches, real apt, real Trash). Instead they
monkeypatch entries of the `cleaners` dict with lightweight fakes and assert
on the dispatch behaviour of cleanSelectedCache() itself.
"""

import cleaner.CleanerEngine as CleanerEngine
from cleaner.TempCleaner import cleanTempFiles


def test_temp_files_is_wired_into_cleaners_dict():
    assert "Temp Files" in CleanerEngine.cleaners
    assert CleanerEngine.cleaners["Temp Files"] is cleanTempFiles


def test_selected_cleaner_is_actually_called(monkeypatch):
    calls = []

    def fake_cleaner():
        calls.append("called")
        return True

    monkeypatch.setitem(CleanerEngine.cleaners, "Temp Files", fake_cleaner)

    results = CleanerEngine.cleanSelectedCache(["Temp Files"])

    assert calls == ["called"]
    assert results == {"Temp Files": True}


def test_multiple_selected_cleaners_are_each_called(monkeypatch):
    calls = []

    monkeypatch.setitem(
        CleanerEngine.cleaners, "Temp Files", lambda: calls.append("temp") or True
    )
    monkeypatch.setitem(
        CleanerEngine.cleaners, "Trash", lambda: calls.append("trash") or False
    )

    results = CleanerEngine.cleanSelectedCache(["Temp Files", "Trash"])

    assert set(calls) == {"temp", "trash"}
    assert results == {"Temp Files": True, "Trash": False}


def test_unknown_cleaner_name_is_handled_without_crash():
    results = CleanerEngine.cleanSelectedCache(["Not A Real Cache"])

    assert results == {"Not A Real Cache": False}


def test_cleaner_exception_is_caught_and_reported_false(monkeypatch):
    def exploding_cleaner():
        raise RuntimeError("boom")

    monkeypatch.setitem(CleanerEngine.cleaners, "Temp Files", exploding_cleaner)

    # Must not raise - cleanSelectedCache wraps each cleaner call.
    results = CleanerEngine.cleanSelectedCache(["Temp Files"])

    assert results == {"Temp Files": False}


def test_mixed_known_and_unknown_selection(monkeypatch):
    monkeypatch.setitem(CleanerEngine.cleaners, "Temp Files", lambda: True)

    results = CleanerEngine.cleanSelectedCache(["Temp Files", "Unknown Cache"])

    assert results == {"Temp Files": True, "Unknown Cache": False}
