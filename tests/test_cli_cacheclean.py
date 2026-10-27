"""
Controlled pytest tests for cli/cacheclean.py's CLI argument handling.

--help / --version / invalid-arg cases are exercised via subprocess, since
argparse exits the process itself for those paths before any TUI code runs
- nothing destructive or interactive is ever reached. Normal-invocation
behaviour is tested in-process with CacheSelectionScreen.run and
EnvironmentChecker.check mocked out, so the real Textual TUI never starts
and no environment/filesystem check actually runs.
"""

import subprocess
import sys

import cli.cacheclean as cacheclean


CLI_PATH = cacheclean.__file__


def _run(args):
    return subprocess.run(
        [sys.executable, CLI_PATH, *args],
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_help_displays_usage_and_exits_zero():
    result = _run(["--help"])

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_help_does_not_launch_tui():
    # If the TUI had started, Textual would try to take over the terminal
    # and this subprocess (no real tty attached) would hang until the
    # 10s timeout or emit Textual/terminal errors - a clean, fast exit
    # with plain argparse usage text is the proof it never launched.
    result = _run(["--help"])

    assert result.returncode == 0
    assert "Professional Ubuntu Cache Cleaning Utility" in result.stdout


def test_version_runs_without_launching_tui():
    result = _run(["--version"])

    assert result.returncode == 0
    assert "cacheclean" in result.stdout.lower()


def test_invalid_argument_returns_nonzero_exit():
    result = _run(["--totally-not-a-real-flag"])

    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_cli_importable_and_runnable_from_other_cwd(tmp_path):
    result = subprocess.run(
        [sys.executable, CLI_PATH, "--help"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(tmp_path),
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_normal_invocation_dispatches_to_app_without_real_startup(monkeypatch):
    calls = []

    class FakeApp:
        def run(self):
            calls.append("ran")

    monkeypatch.setattr(cacheclean, "CacheSelectionScreen", lambda: FakeApp())
    monkeypatch.setattr(
        cacheclean.EnvironmentChecker, "check", lambda self: []
    )
    monkeypatch.setattr(sys, "argv", ["cacheclean"])

    cacheclean.main()

    assert calls == ["ran"]


def test_startup_exception_is_logged_and_exits_nonzero(monkeypatch):
    logged = []

    monkeypatch.setattr(
        cacheclean.EnvironmentChecker,
        "check",
        lambda self: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    monkeypatch.setattr(cacheclean.CrashLogger, "log", lambda e: logged.append(e))
    monkeypatch.setattr(sys, "argv", ["cacheclean"])

    try:
        cacheclean.main()
        assert False, "main() should have called sys.exit(1)"
    except SystemExit as exc:
        assert exc.code == 1

    assert len(logged) == 1
    assert isinstance(logged[0], RuntimeError)
