# TINO — Terminal Dino Endless Runner 🦖

[![CI](https://github.com/your-org/tino/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/tino/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**TINO** is a high-performance, terminal-based endless runner inspired by Chrome's offline Dino game. Built natively with Python standard library `curses`, it runs smoothly on macOS and Linux (across Bash, Zsh, and any modern terminal emulator).

---

## 🎮 Features

- **Instant Terminal Diversion**: Jump straight in with `tino` — zero mandatory configuration or heavy runtime dependencies.
- **Decoupled Engine**: Core game logic (collision, gravity, speed scaling, state transitions) is 100% separated from the curses renderer and fully unit-testable.
- **Progressive Difficulty**: Speed and obstacle spawn rates scale dynamically with elapsed survival time.
- **Local Persistence**: Cross-platform JSON high score storage (`~/Library/Application Support/tino` on macOS, XDG on Linux).
- **CLI Utilities**: Standalone stdout commands `tino score` and `tino reset-score` for quick checks and scripting.

---

## 🕹️ Controls

| Key | Action |
|:---|:---|
| <kbd>Space</kbd> / <kbd>↑</kbd> / <kbd>Enter</kbd> | Jump / Start Game |
| <kbd>r</kbd> | Restart (at Game Over screen) |
| <kbd>q</kbd> / <kbd>Ctrl+C</kbd> | Quit safely at any time |

---

## 🚀 Quickstart

### Prerequisites
- Python **3.12+**
- macOS or Linux (Bash / Zsh)

### 1. Clone & Setup
```bash
git clone https://github.com/your-org/tino.git
cd tino

# Run automatic setup script
./scripts/setup.sh

# Activate virtual environment
source .venv/bin/activate
```

### 2. Play
```bash
# Launch the game directly
tino
```

### 3. CLI Commands
```bash
# View current high score
tino score

# Reset high score
tino reset-score

# Check version
tino --version
```

---

## 📂 Project Architecture

```
tino/
├── src/tino/
│   ├── cli.py              # CLI argument parsing (argparse)
│   ├── app.py              # Game loop orchestrator & curses lifecycle
│   ├── config.py           # Configuration loader & defaults
│   ├── engine/             # Terminal-agnostic game logic
│   │   ├── game.py         # Main Game state coordinator & tick runner
│   │   ├── state.py        # State machine (MENU, PLAYING, GAME_OVER)
│   │   ├── entities.py     # Player (jump physics) & Obstacle
│   │   ├── collision.py    # Pure AABB collision detection
│   │   └── difficulty.py   # Dynamic speed & spawn progression
│   ├── ui/                 # Curses presentation layer
│   │   ├── terminal.py     # Safe curses init/teardown & size checks
│   │   ├── renderer.py     # ASCII rendering & HUD overlays
│   │   └── input.py        # Non-blocking input to Action mapper
│   └── storage/            # Data persistence
│       ├── paths.py        # Cross-platform data directory resolver
│       └── highscore.py    # HighScoreStore protocol & JSON store
├── tests/
│   ├── unit/               # Unit tests (no terminal needed)
│   └── integration/        # CLI & app wiring tests
├── scripts/
│   ├── setup.sh            # Setup venv & dependencies
│   ├── lint.sh             # Ruff linter & formatter
│   └── test.sh             # pytest test runner
├── docs/                   # Complete architectural documentation
├── .github/workflows/      # GitHub Actions CI
└── pyproject.toml          # Build configuration & dev tooling
```

---

## 🧪 Testing & Quality Assurance

```bash
# Run all unit and integration tests
./scripts/test.sh

# Run Ruff linter and formatter
./scripts/lint.sh
```

---

## 👥 Team Work & Contributing

Are you collaborating with teammates on this project?
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for branch strategy, PR workflows, and code guidelines.
- Check [docs/TEAM_TASKS.md](docs/TEAM_TASKS.md) for the work distribution matrix and roadmap feature assignments.
- Read full architectural specifications in the [`docs/`](docs/) directory.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
