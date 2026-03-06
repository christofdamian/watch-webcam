# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

watch-webcam is a Python CLI tool that monitors webcam usage (via `fuser` on `/dev/video*` devices) and triggers configurable actions when a video call starts/stops. Actions include toggling Elgato key lights, pausing media, disabling xscreensaver, and running custom scripts.

## Build & Install

```bash
pip install -e .           # editable install
pip install -e ".[dev]"    # if dev dependencies are added
```

The package uses setuptools with `pyproject.toml`. Entry point: `watch-webcam` CLI command maps to `watch_webcam.cli:main`.

## Running Tests

```bash
pytest                     # run all tests
pytest tests/watch_webcam/actions/test_light.py  # run a single test file
pytest -k test_discover    # run tests matching a pattern
```

Tests use `unittest.mock` (Mock, patch) for mocking external dependencies like `leglight` and `subprocess`.

## Architecture

The main loop in `cli.py` polls video devices every second, detects state changes, and calls actions:

- **`Video`** (`video.py`) — uses `fuser -v` to check if known applications (zoom, firefox, teams, etc.) are accessing video devices.
- **Actions** (`actions/`) — all inherit from `actions/base.py:Base` which defines three hooks:
  - `discover()` — called once at startup (e.g., find Elgato lights on the network)
  - `while_on()` — called every loop iteration while webcam is active (e.g., keep xscreensaver deactivated)
  - `switch(new_state)` — called on state transitions (on/off)
- **Action implementations**: `Light` (Elgato via leglight), `Media` (playerctl pause), `XScreenSaver` (xscreensaver-command), `Script` (run arbitrary shell commands)

Configuration is loaded from a YAML file (default: `watch-webcam.yml`). Each action has an `enabled` flag in the config.

## Dependencies

- `leglight` — Elgato Key Light control
- `pyyaml` — YAML config parsing
- `pytest` — testing
