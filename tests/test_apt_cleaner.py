"""
Controlled pytest tests for cleaner.AptCleaner.CleanaptCheck().

Replaces tests/testAptfiles.py. CleanaptCheck() shells out to the real
`apt clean` command when running as root. These tests never allow a real
apt invocation: subprocess.run is always monkeypatched to a fake before
CleanaptCheck() is called, and isRootUser is monkeypatched to control which
branch is exercised.
"""

import cleaner.AptCleaner as AptCleaner


class _FakeCompletedProcess:
    def __init__(self, returncode, stderr=""):
        self.returncode = returncode
        self.stderr = stderr


def test_non_root_never_invokes_apt(monkeypatch):
    monkeypatch.setattr(AptCleaner, "isRootUser", lambda: False)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("subprocess.run must not be called when not root")

    monkeypatch.setattr(AptCleaner.subprocess, "run", fail_if_called)

    assert AptCleaner.CleanaptCheck() is False


def test_root_and_apt_success_returns_true(monkeypatch):
    monkeypatch.setattr(AptCleaner, "isRootUser", lambda: True)

    calls = []

    def fake_run(cmd, capture_output=True, text=True):
        calls.append(cmd)
        return _FakeCompletedProcess(returncode=0)

    monkeypatch.setattr(AptCleaner.subprocess, "run", fake_run)

    assert AptCleaner.CleanaptCheck() is True
    assert calls == [["apt", "clean"]]


def test_root_and_apt_failure_does_not_return_true(monkeypatch):
    monkeypatch.setattr(AptCleaner, "isRootUser", lambda: True)
    monkeypatch.setattr(
        AptCleaner.subprocess,
        "run",
        lambda *a, **k: _FakeCompletedProcess(returncode=1, stderr="failed"),
    )

    # Documents actual current behaviour: on a non-zero apt return code the
    # function falls through without an explicit return (implicit None).
    # It must never be True/truthy in this branch.
    assert not AptCleaner.CleanaptCheck()


def test_subprocess_exception_is_caught_and_returns_false(monkeypatch):
    monkeypatch.setattr(AptCleaner, "isRootUser", lambda: True)

    def raising_run(*args, **kwargs):
        raise OSError("apt not found")

    monkeypatch.setattr(AptCleaner.subprocess, "run", raising_run)

    assert AptCleaner.CleanaptCheck() is False
