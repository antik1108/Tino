# TINO — Terminal Dino Endless Runner 🦖

[![CI](https://github.com/antik1108/Tino/actions/workflows/ci.yml/badge.svg)](https://github.com/antik1108/Tino/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

TINO is a terminal-based endless runner inspired by Chrome's offline Dino game. It runs entirely inside your terminal — no browser, no GUI, no external runtime. Just Python and your keyboard.

```
  _____ _____ _   _  ____
 |_   _|_   _| \ | |/ __ \
   | |   | | |  \| | |  | |
   | |   | | | . ` | |  | |
   |_|  |___|_|\_\_|\____/

      TERMINAL DINO ENDLESS RUNNER
         ▶  PRESS SPACE TO START  ◀
```

---

## What it looks like

- A dino auto-runs left to right across the terminal.
- Cactus obstacles scroll toward you. Press **Space** to jump.
- Speed increases the longer you survive. One hit ends the run.
- Your high score is saved locally between sessions.

---

## Requirements

- **Python 3.12 or newer** — check with `python3 --version`
- **macOS or Linux** (any modern terminal emulator)
- **Terminal size**: at least 60 columns × 16 rows

---

## Setup after cloning

```bash
# 1. Clone the repo
git clone https://github.com/antik1108/Tino.git
cd Tino

# 2. Create a virtual environment and install everything
./scripts/setup.sh

# 3. Activate the virtual environment
source .venv/bin/activate
```

That's it. The `setup.sh` script creates a `.venv`, upgrades pip, and installs TINO plus its dev dependencies (`pytest` and `ruff`) in editable mode.

> **Windows note:** TINO uses the `curses` library which is not available on Windows by default. macOS and Linux are fully supported.

---

## Playing the game

```bash
tino
```

Press **Space** or **↑** to start. The game begins immediately.

### Controls

| Key | Action |
|:---|:---|
| `Space` / `↑` / `Enter` | Jump (and start the game from the menu) |
| `r` | Restart — only on the Game Over screen |
| `q` / `Ctrl+C` | Quit cleanly at any time |

---

## CLI commands

```bash
# Launch the game
tino

# Print your current stored high score (no terminal takeover)
tino score

# Reset your high score back to 0 (asks for confirmation)
tino reset-score

# Skip confirmation prompt
tino reset-score --force

# Check the installed version
tino --version

# Help
tino --help
```

---

## Running the tests

```bash
./scripts/test.sh
```

This runs the full pytest suite (34 tests covering collision, entities, difficulty, state machine, high score storage, config loading, and CLI wiring). No terminal is required — the engine is fully isolated from curses.

---

## Linting

```bash
./scripts/lint.sh
```

Uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting. The CI pipeline runs this on every push.

---

## Optional: custom key bindings

Create a config file at the path shown below and TINO will merge it over the defaults on startup. The file is entirely optional — the game runs fine without it.

**macOS:** `~/Library/Application Support/tino/config.json`  
**Linux:** `~/.local/share/tino/config.json`

```json
{
  "keybindings": {
    "jump": "space",
    "quit": "q",
    "restart": "r"
  },
  "target_fps": 30
}
```

Only the keys you include are overridden. Unknown keys are silently ignored, so the file is forward-compatible.

---

## Project structure

```
tino/
├── src/tino/
│   ├── cli.py              # CLI entry point (argparse)
│   ├── app.py              # Game loop — wires engine + UI + storage
│   ├── config.py           # Defaults + optional config file loading
│   ├── engine/             # Pure game logic — no curses dependency
│   │   ├── game.py         # State machine + tick coordinator
│   │   ├── state.py        # GameState enum + transition rules
│   │   ├── entities.py     # Player (jump physics) and Obstacle
│   │   ├── collision.py    # AABB collision detection
│   │   └── difficulty.py   # Speed + spawn rate progression
│   ├── ui/                 # Terminal presentation layer
│   │   ├── terminal.py     # Safe curses init/teardown + resize handling
│   │   ├── renderer.py     # ASCII rendering: menu, gameplay, game-over
│   │   └── input.py        # Non-blocking key reads → engine Actions
│   └── storage/
│       ├── highscore.py    # HighScoreStore protocol + JSON implementation
│       └── paths.py        # Cross-platform data directory resolver
├── tests/
│   ├── unit/               # Engine + storage tests (no terminal needed)
│   └── integration/        # CLI and app wiring checks
├── scripts/
│   ├── setup.sh            # Create venv + install deps
│   ├── lint.sh             # Run Ruff
│   └── test.sh             # Run pytest
├── docs/                   # Full architecture and design documentation
├── .github/workflows/      # GitHub Actions CI (lint + tests on every push)
└── pyproject.toml          # Build config, dependencies, tool settings
```

---

## How high scores are stored

Scores are saved as a JSON file in your user data directory — no database, no cloud:

- **macOS:** `~/Library/Application Support/tino/highscore.json`
- **Linux:** `~/.local/share/tino/highscore.json`

A missing or corrupted file is treated as zero — the game never crashes on a bad score file.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch strategy, PR guidelines, and code standards. The [docs/](docs/) folder contains the full architecture, game design, and requirements documents.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
