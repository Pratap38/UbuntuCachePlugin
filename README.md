# Ubuntu Cache Cleaner



<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/textual-TUI-111111?style=for-the-badge" alt="Textual TUI">
  <img src="https://img.shields.io/badge/rich-terminal_UI-0080FF?style=for-the-badge" alt="Rich terminal UI">
  <img src="https://img.shields.io/badge/status-active-2E7D32?style=for-the-badge" alt="Project status">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge" alt="License">
</p>
<p align="center">
  <img width="1052" height="602" alt="Ubuntu_Cache_Cleaner_Demo" src="https://github.com/user-attachments/assets/454043e9-dfa8-44de-92a5-9c3e8e9fa44d" />
  
 
 
</p>
<p align="center">
  <strong>A polished terminal app for scanning Ubuntu cache, guiding safe cleanup, and generating clear reports.</strong>
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

## Why It Exists

Cache cleanup is often simple in theory and confusing in practice.

This project exists to make the process:

- visible
- explainable
- recoverable
- beginner-friendly
- useful for daily maintenance

The goal is to reduce guesswork without taking away control.

## Highlights

| Area | What You Get |
| --- | --- |
| Scanning | Detects and analyzes cache categories |
| Cleaning | Uses focused cleaner modules for specific targets |
| UI | A guided terminal interface built with Textual |
| Safety | Permission checks and safer delete workflows |
| Insight | Recommendation and auto-detection support |
| Reliability | Logging, recovery, and reporting helpers |

## Key Features

- Scans Ubuntu cache and temporary storage categories
- Supports multiple cleaner modules for different cache sources
- Uses a terminal UI for interactive workflows
- Shows cleaning summaries and final reports
- Includes recommendation and auto-detection engines
- Tracks recovery and crash-related logs
- Uses permission checks before sensitive operations
- Provides a modular codebase for future expansion

## Screenshots


- `<img width="1262" height="724" alt="image" src="https://github.com/user-attachments/assets/1c7b7464-948c-4bed-a266-e1811c98486b" />

- `<img width="1313" height="909" alt="image" src="https://github.com/user-attachments/assets/9127b252-3290-4bfd-a3a9-9d0b15c2590c" />



## Architecture

```text
                         Ubuntu Cache Cleaner
                                  |
           -------------------------------------------------
           |                |               |               |
      Scanner Engine   Cleaner Engine   Safety Layer   TUI Screens
           |                |               |               |
           -------------------------------------------------
                                  |
                           Final Report
```

## Workflow

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
|-- config/
|-- install.sh
|-- uninstall.sh
|-- setup.py
`-- requirements.txt
```

### Main Modules

- `main.py` starts the application
- `cli/cacheclean.py` exposes the command-line entry point
- `ui/` contains the Textual-based screens and widgets
- `Scanner/` contains scan logic and scan orchestration
- `cleaner/` contains cleanup implementations
- `core/` contains configuration, logging, detection, permissions, and reporting helpers

## Installation

### Requirements

- Ubuntu or another Linux distribution
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

This opens the interactive terminal application.

## Interactive TUI Usage

The app is organized around a guided terminal flow:

- dashboard and navigation screens
- cache category selection
- live or staged scanning
- progress indicators
- report generation
- cleaner actions with safety checks

## Configuration

Configuration lives in:

```text
config/config.json
```

Typical options include:

- recommendation visibility
- auto-detection visibility
- cleanup behavior toggles
- report display preferences

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

## Recommendation Engine

The recommendation engine helps explain scan output and suggests next actions based on detected cache categories and system state.

## Auto Detection

Auto-detection surfaces warnings and useful system observations during reporting, so users can see potential issues without digging through raw output.

## Crash Recovery

The project includes crash and recovery helpers so failures can be logged and analyzed instead of disappearing silently.

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

## Threading

If concurrency is expanded later, it should stay focused on safe parallel work and avoid overlapping deletion on the same paths.

## Rich UI

Rich is used for polished terminal rendering, readable output, and visually clear status information.

## Textual UI

Textual powers the interactive screen flow and gives the app a modern terminal experience.

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

If installed in editable mode:

```bash
pip uninstall Baker
```

If installed from a system package or executable bundle, remove it using the matching install method.

## Troubleshooting

- Make sure the virtual environment is activated before launching the app
- Confirm your user has permission to inspect the relevant cache paths
- If a screen fails to load, check terminal size and installed dependencies
- Review logs when cleanup or recovery behavior does not match expectations

## FAQ

### Is it safe to use?

The project is designed around guided cache cleanup. Review the selected categories before deleting anything.

### Does it delete personal files?

It is intended to target cache and temporary data, not personal documents. Always verify selected paths before cleanup.

### Can I extend it?

Yes. The codebase is modular and meant to grow with new scanners, cleaner modules, and UI screens.

## Security

System cleanup tools should be treated carefully.

- validate paths before deleting
- keep permission checks in place
- log failures and skipped items
- avoid unsafe recursive deletion patterns

## Roadmap

Planned areas for future improvement:

- more refined cleaning presets
- expanded scanning coverage
- richer report visuals
- stronger recovery tooling
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

Add the project license here, or link to the repository license file when available.

## Credits

Built by Pratap and contributors.

Special thanks to the Python, Rich, and Textual ecosystems for making terminal applications enjoyable to build.
