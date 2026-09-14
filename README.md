# Ubuntu Cache Cleaner



<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/textual-TUI-111111?style=for-the-badge" alt="Textual TUI">
  <img src="https://img.shields.io/badge/rich-terminal_UI-0080FF?style=for-the-badge" alt="Rich terminal UI">
  <img src="https://img.shields.io/badge/RAM_Guardian-systemd_service-4B32C3?style=for-the-badge" alt="RAM Guardian systemd service">
  <img src="https://img.shields.io/badge/status-active-2E7D32?style=for-the-badge" alt="Project status">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge" alt="License">
</p>
<p align="center">
  <img width="1052" height="602" alt="Ubuntu_Cache_Cleaner_Demo" src="https://github.com/user-attachments/assets/454043e9-dfa8-44de-92a5-9c3e8e9fa44d" />
  
 
 
</p>
<p align="center">
  <strong>A polished terminal app for scanning Ubuntu cache, guiding safe cleanup, and generating clear reports — with a background RAM Guardian that keeps your system responsive under memory pressure.</strong>
</p>

<p align="center">
  Fast. Safe. Explainable.
</p>

---

## Overview

Ubuntu Cache Cleaner is a Python terminal application for Ubuntu systems that helps users inspect cache usage, understand cleanup risk, and run guided removal workflows through a modern TUI.

It blends:

- category-based cache scanning
- safety-first cleanup modules
- recommendation and auto-detection logic
- recovery and logging support
- Textual and Rich-powered interfaces
- **RAM Guardian** — a self-contained background subsystem that monitors system memory and pauses (never kills) the least-recently-used application under memory pressure, running as a real `systemd --user` service

## Why It Exists

Cache cleanup is often simple in theory and confusing in practice, and runaway memory pressure is a second, related problem existing tools only react to after the system is already struggling.

This project exists to make both processes:

- visible
- explainable
- recoverable
- beginner-friendly
- useful for daily maintenance

The goal is to reduce guesswork without taking away control.

## What We Are Building

We are currently building a Linux system-maintenance assistant with two cooperating halves:

**Cache Cleaner** helps users:

- detect cache and temporary files
- understand what is safe to remove
- clean selected items through a guided terminal workflow
- see clear summaries and reports after cleanup
- recover and debug issues when something goes wrong

**RAM Guardian** helps users:

- avoid system freezes from runaway memory usage
- get non-destructive relief (pause via `SIGSTOP`, not kill) under memory pressure
- automatically resume a paused application the moment they focus it again
- see exactly what happened and why, through desktop notifications and logs
- run continuously in the background as an installed, singleton-protected service — no manual startup required

The focus is on keeping both processes simple for everyday users while still giving enough detail for contributors and power users to trust what the tool is doing.

## Problem Statement

Linux users often accumulate cache, temporary files, and app-specific clutter over time. Manually identifying these files can be confusing, and deleting them without context can feel risky. Separately, memory-heavy applications — browsers, IDEs, media players — can quietly consume gigabytes of RAM until the system starts thrashing, with no warning until it's already too late.

This project solves both problems: a structured, safe, and explainable way to inspect and clean cache data from the terminal, and a proactive background guardian that keeps memory pressure from turning into a frozen desktop.

## Highlights

| Area | What You Get |
| --- | --- |
| Scanning | Detects and analyzes cache categories |
| Cleaning | Uses focused cleaner modules for specific targets |
| UI | A guided terminal interface built with Textual, with live RAM Guardian status |
| Safety | Permission checks, safer delete workflows, and non-destructive process pausing |
| Insight | Recommendation and auto-detection support |
| Reliability | Logging, recovery, persistence, and crash-safe restart behavior |
| Memory protection | RAM Guardian pauses idle memory-heavy apps and auto-resumes them on focus |

## Key Features

- Scans Ubuntu cache and temporary storage categories
- Supports multiple cleaner modules for different cache sources
- Uses a terminal UI for interactive workflows, including a live Guardian status indicator
- Shows cleaning summaries and final reports
- Includes recommendation and auto-detection engines
- Tracks recovery and crash-related logs
- Uses permission checks before sensitive operations
- Provides a modular codebase for future expansion
- Monitors system RAM continuously and classifies pressure into Normal / Warning / Critical / Emergency
- Pauses (never kills) the least-recently-used, non-whitelisted process under critical memory pressure
- Automatically resumes a paused process once it regains window focus or RAM returns to a safe level
- Persists pause state to disk and survives Guardian restarts and crashes without losing track of paused processes
- Runs as a `systemd --user` background service, installed and enabled automatically

## Screenshots


- `<img width="1262" height="724" alt="image" src="https://github.com/user-attachments/assets/1c7b7464-948c-4bed-a266-e1811c98486b" />

- `<img width="1313" height="909" alt="image" src="https://github.com/user-attachments/assets/9127b252-3290-4bfd-a3a9-9d0b15c2590c" />



## Architecture

```text
                              Ubuntu Cache Cleaner
                                       |
          -----------------------------------------------------------
          |                |               |               |        |
     Scanner Engine   Cleaner Engine   Safety Layer   TUI Screens  RAM Guardian
          |                |               |               |        |
          -----------------------------------------------------------
                                       |
                                Final Report / Live Guardian Status
```

RAM Guardian itself runs as an independent background service, not inside the TUI process:

```text
                        systemd --user
                              |
                 ubuntu-cache-cleaner-guardian.service
                              |
                    Guardian.GuardianDaemon
                     (flock singleton guard)
                              |
                       GuardianEngine
                     /        |         \
             RAMMonitor  DecisionEngine  PauseManager / ResumeManager
                     \        |         /
                    GuardianConfig + GuardianPaths + PauseRegistry
                    (~/.config & ~/.local/state/ubuntu-cache-cleaner/)
```

## Workflow

**Cache Cleaner (interactive):**

```text
Start
  |
  v
Check permissions
  |
  v
Scan cache categories
  |
  v
Analyze risk and recommendations
  |
  v
Choose cleaning preset
  |
  v
Run safe cleanup
  |
  v
Generate final report
```

**RAM Guardian (background loop, every `monitorInterval` seconds):**

```text
Read current RAM usage
  |
  v
Classify pressure (Normal / Warning / Critical / Emergency)
  |
  v
Resume any eligible paused process first (if RAM is safe again)
  |
  v
If still critical and no resume happened this tick:
  select least-recently-used, non-whitelisted candidate
  |
  v
Pause it with SIGSTOP, persist to registry, notify the user
  |
  v
Wait for focus or safe RAM, then resume automatically with SIGCONT
```

## Project Structure

```text
.
|-- main.py
|-- cli/
|-- core/
|-- cleaner/
|-- Scanner/
|-- ui/
|-- tests/
|-- Guardian/
|   |-- GuardianEngine.py
|   |-- GuardianDaemon.py
|   |-- GuardianOrchestrator.py
|   |-- GuardianConfig.py
|   |-- GuardianPaths.py
|   |-- PauseManager.py / ResumeManager.py
|   |-- PauseRegistry.py
|   |-- WhitelistManager.py / NotificationManager.py
|   |-- Focus/ / platform/x11/ / platform/Wayland/
|   `-- tests/
|-- systemd/
|   `-- ubuntu-cache-cleaner-guardian.service   (template)
|-- config/
|-- install.sh
|-- uninstall.sh
|-- install-gnome-extension.sh
|-- setup.py
`-- requirements.txt
```

### Main Modules

- `main.py` starts the application
- `cli/cacheclean.py` exposes the command-line entry point
- `ui/` contains the Textual-based screens and widgets, including the Guardian status indicator
- `Scanner/` contains scan logic and scan orchestration
- `cleaner/` contains cleanup implementations
- `core/` contains configuration, logging, detection, permissions, reporting helpers, and `GuardianStatus` (the dashboard's read-only Guardian status check)
- `Guardian/` contains the entire RAM Guardian subsystem — engine, daemon, config, persistence, pause/resume, focus tracking, and its own test suite, kept self-contained from the cache-cleaning code
- `systemd/ubuntu-cache-cleaner-guardian.service` is the installer-owned service template (`@PROJECT_ROOT@` / `@PYTHON_EXECUTABLE@` placeholders), substituted with real paths at install time

## Installation

### Requirements

- Ubuntu or another Linux distribution with a `systemd --user` session
- Python 3.12 or newer
- `pip`
- `venv` recommended

### From Source

```bash
git clone <repo-url>
cd UbuntuCacheCLeaner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Using the Installer Script

```bash
bash install.sh
```

This does more than a plain `pip install`. It:

1. Installs Python dependencies (`rich`, `textual`, `psutil`, `plotext`)
2. Installs Ubuntu Cache Cleaner itself in editable mode
3. Detects the actual project root and Python interpreter it is running with — never a hard-coded path
4. Generates a real `ubuntu-cache-cleaner-guardian.service` from the `systemd/` template using those detected values
5. Installs it to `~/.config/systemd/user/`, reloads the systemd user daemon, and enables + starts RAM Guardian immediately

After installation, RAM Guardian is already running in the background — no separate step needed.

### Installing the RAM Guardian GNOME Extension

If you are testing focus detection, install the GNOME Shell extension into the
active session data directory:

```bash
bash install-gnome-extension.sh
```

This installs to `${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions/`
so it works even when your terminal overrides `XDG_DATA_HOME` (for example, when
running inside a Snap-managed editor terminal).

## Quick Start

```bash
source venv/bin/activate
cacheclean
```

Or run the entry script directly:

```bash
python3 main.py
```

## CLI Usage

The installed command is:

```bash
cacheclean
```

This opens the interactive terminal application. RAM Guardian runs independently as a background service and does not need `cacheclean` to be open.

## Interactive TUI Usage

The app is organized around a guided terminal flow:

- dashboard and navigation screens, including a `RAM Guardian: Running / Stopped / Not installed` status line
- cache category selection
- live or staged scanning
- progress indicators
- report generation
- cleaner actions with safety checks

The dashboard only *observes* Guardian's `systemd --user` service state (via `systemctl --user is-active`, falling back gracefully if systemd or the service is unavailable) — it never starts a second Guardian process itself.

## Configuration

Cache Cleaner configuration lives in:

```text
config/config.json
```

Typical options include:

- recommendation visibility
- auto-detection visibility
- cleanup behavior toggles
- report display preferences

RAM Guardian has its own, separate configuration file (see below), since it runs as an independent service with its own lifecycle.

## RAM Guardian

RAM Guardian is a self-contained subsystem under `Guardian/` that monitors system memory in real time and pauses — never kills — the least-recently-used, non-critical application when memory pressure crosses a configurable threshold, then resumes it automatically once you focus it again or RAM returns to a safe level.

### Why pause instead of kill?

- **No data loss** — a paused process's memory state is fully preserved; nothing in it is lost
- **Instant recovery** — resuming with `SIGCONT` is immediate, no restart or reload
- **Transparent** — the user is notified when it happens and why, and the app simply "comes back" when refocused

### Configuration

RAM Guardian's configuration lives at:

```text
~/.config/ubuntu-cache-cleaner/guardian_config.json
```

| Key | Default | Meaning |
| --- | --- | --- |
| `enabled` | `true` | Master on/off switch for the Guardian |
| `warningThreshold` | `80` | RAM % at which the Warning state begins |
| `criticalThreshold` | `90` | RAM % at which Guardian starts pausing candidates |
| `emergencyThreshold` | `97` | Highest alert level |
| `monitorInterval` | `2` | Seconds between memory checks |
| `autoPause` | `true` | Allow Guardian to pause processes automatically |
| `autoResume` | `true` | Allow Guardian to resume paused processes automatically |
| `resumeThreshold` | `75` | RAM % at or below which a paused process becomes resumable |
| `desktopNotifications` | `true` | Show a desktop notification on pause/resume |
| `logEvents` | `true` | Record pause/resume events to history |
| `whitelist` | `systemd`, `gnome-shell`, `Xorg`, `pipewire`, `dbus-daemon`, `NetworkManager`, `RAM Guardian` | Processes Guardian will never pause |

Guardian's runtime state lives separately, under:

```text
~/.local/state/ubuntu-cache-cleaner/
├── guardian_state.json     # persisted pause registry, survives restarts
├── guardian.lock           # singleton lock (flock)
└── logs/guardian.log
```

### Managing the Guardian service

```bash
# Check status
systemctl --user status ubuntu-cache-cleaner-guardian.service

# Stop / start manually
systemctl --user stop ubuntu-cache-cleaner-guardian.service
systemctl --user start ubuntu-cache-cleaner-guardian.service

# Disable / re-enable auto-start at login
systemctl --user disable ubuntu-cache-cleaner-guardian.service
systemctl --user enable ubuntu-cache-cleaner-guardian.service
```

Guardian is singleton-protected: if a second instance is ever started (manually or after a race), it detects the existing lock, prints `RAM Guardian is already running.`, and exits immediately rather than running two monitors side by side. A hard crash releases the lock automatically, and `systemd`'s `Restart=on-failure` brings Guardian back up with a fresh PID that reacquires it cleanly.

### Focus tracking

On Wayland sessions, RAM Guardian determines which window currently has focus through a GNOME Shell extension (see [Installing the RAM Guardian GNOME Extension](#installing-the-ram-guardian-gnome-extension)) that reports focus changes over a local Unix domain socket — never by bypassing Wayland's security model. This is what lets Guardian avoid pausing the application you're actively using, and resume a paused one the moment you switch back to it.

## Cleaning Presets

Presets help users choose the right level of cleanup without manually selecting every category.

Expected preset styles:

- safe cleanup
- balanced cleanup
- aggressive cleanup

## Safety Features

Ubuntu Cache Cleaner is built with safety in mind:

- permission checks before sensitive actions
- cleaner separation by cache type
- structured reporting
- error handling around scanner and recommendation workflows
- recovery logging support

RAM Guardian adds its own, independent safety layer:

- never touches whitelisted or system-critical processes
- never terminates a process — only suspends and resumes it
- persists ownership of paused processes to disk so a Guardian restart never "loses" one
- verifies process identity (PID + start time) before resuming, so a reused PID is never mistaken for the process Guardian originally paused
- singleton-locked so two Guardian instances can never race each other

## Recommendation Engine

The recommendation engine helps explain scan output and suggests next actions based on detected cache categories and system state.

## Auto Detection

Auto-detection surfaces warnings and useful system observations during reporting, so users can see potential issues without digging through raw output.

## Crash Recovery

The project includes crash and recovery helpers so failures can be logged and analyzed instead of disappearing silently. RAM Guardian has its own equivalent: a persisted pause registry that a fresh Guardian instance reloads and verifies after any restart or crash.

## Recovery Logs

Recovery logging is intended to support:

- post-failure diagnosis
- cleanup session traceability
- debugging permission and deletion issues

## Performance

The project favors practical terminal performance:

- modular scanning
- lightweight text UI rendering
- targeted cleanup operations
- small dependency footprint

RAM Guardian itself is intentionally lightweight — a single Python process polling memory every few seconds, well under 20 MB resident at idle.

## Threading

If concurrency is expanded later, it should stay focused on safe parallel work and avoid overlapping deletion on the same paths.

## Rich UI

Rich is used for polished terminal rendering, readable output, and visually clear status information.

## Textual UI

Textual powers the interactive screen flow and gives the app a modern terminal experience, including the live RAM Guardian status widget on the main screen.

## Development Guide

For local development:

```bash
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
python3 main.py
```

## Testing

Run the available tests with:

```bash
pytest
```

Most of the Guardian test suite under `Guardian/tests/` is written as standalone scripts rather than pytest-discoverable functions; run those individually, e.g.:

```bash
PYTHONPATH=. python3 Guardian/tests/test_guardian_engine.py
```

You can also target specific checks when iterating on a module.

## Build Executable

This project can be packaged into a standalone executable with tools such as PyInstaller.

Example:

```bash
pyinstaller --onefile main.py
```

## Packaging

The project includes a `setup.py` and console script entry point:

```text
cacheclean=cli.cacheclean:main
```

Packaging uses `find_namespace_packages()` (not `find_packages()`) so that Guardian's sub-packages — `Guardian.models`, `Guardian.Focus`, `Guardian.platform`, `Guardian.platform.x11`, `Guardian.platform.Wayland` — are correctly discovered even without `__init__.py` files in every directory, while `Guardian.tests` is explicitly excluded from any built distribution.

Install locally in editable mode during development:

```bash
pip install -e .
```

## Installing with pip

```bash
pip install .
```

Or install from a built distribution artifact if one is published later.

## Installing the Executable

If you distribute a compiled binary, place it somewhere in your `PATH`, or install it using your preferred packaging workflow.

## Uninstall

Using the uninstaller script (recommended — this is the only path that also removes RAM Guardian):

```bash
bash uninstall.sh
```

This stops and disables the Guardian service, removes its systemd unit file, deletes its config and state directories under `~/.config/ubuntu-cache-cleaner/` and `~/.local/state/ubuntu-cache-cleaner/` (config, state, lock, and logs), then uninstalls the `Baker` package and cleans build artifacts. It is safe to run even if Guardian was already stopped, disabled, or its service file was already removed.

If installed in editable mode without the uninstaller:

```bash
pip uninstall Baker
```

Note that this alone will **not** remove the Guardian systemd service or its runtime files — use `uninstall.sh` for a complete removal.

## Troubleshooting

- Make sure the virtual environment is activated before launching the app
- Confirm your user has permission to inspect the relevant cache paths
- If a screen fails to load, check terminal size and installed dependencies
- Review logs when cleanup or recovery behavior does not match expectations
- If the dashboard shows `RAM Guardian: Not installed`, run `bash install.sh` again, or check that `~/.config/systemd/user/ubuntu-cache-cleaner-guardian.service` exists
- If Guardian shows `Stopped` unexpectedly, check `systemctl --user status ubuntu-cache-cleaner-guardian.service --no-pager` and `journalctl --user -u ubuntu-cache-cleaner-guardian.service` for the reason
- A second manual launch of `python3 -m Guardian.GuardianDaemon` prints `RAM Guardian is already running.` and exits — this is expected singleton behavior, not an error

## FAQ

### Is it safe to use?

The project is designed around guided cache cleanup. Review the selected categories before deleting anything.

### Does it delete personal files?

It is intended to target cache and temporary data, not personal documents. Always verify selected paths before cleanup.

### Will RAM Guardian ever close an app or lose my work?

No. Guardian only ever suspends a process with `SIGSTOP` and resumes it with `SIGCONT` — it never sends a kill signal, so in-memory state (including unsaved work still held in RAM) is preserved exactly as it was.

### Can I extend it?

Yes. The codebase is modular and meant to grow with new scanners, cleaner modules, UI screens, and Guardian focus-tracking backends (only Wayland is implemented today; X11 support is deliberately left unbuilt for now).

## Security

System cleanup tools should be treated carefully.

- validate paths before deleting
- keep permission checks in place
- log failures and skipped items
- avoid unsafe recursive deletion patterns

RAM Guardian follows the same posture: it works with Wayland's security model rather than around it (no injected code, no reading another application's memory, no elevated privileges for basic focus detection), and its whitelist guarantees it can never pause a process the desktop session itself depends on.

## Roadmap

Planned areas for future improvement:

- more refined cleaning presets
- expanded scanning coverage
- richer report visuals
- X11 focus-tracking backend for RAM Guardian (currently Wayland-only)
- packaging polish — declaring `psutil`/`plotext` consistently across `setup.py` and `requirements.txt`, and shipping Guardian's bundled config via proper package data
- packaging and distribution polish

## Contributing

Contributions are welcome.

Suggested workflow:

1. Fork the repository
2. Create a feature branch
3. Make focused changes
4. Add or update tests
5. Open a pull request with a clear description

## License

This project is licensed under the MIT License. See the [`LICENSE`](/home/pratap/Desktop/UbuntuCacheCLeaner/LICENSE) file for full terms.

## Credits

Built by Pratap and contributors.

Special thanks to the Python, Rich, Textual, and GNOME Shell ecosystems for making both a modern terminal application and a safe desktop-integrated background service possible.
