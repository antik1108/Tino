# Contributing to TINO

Welcome to the **TINO** project! This guide explains how our team works together, branch conventions, and how to pick up modules and tasks.

---

## 🏗️ Architecture Philosophy

Before writing code, please review the documents in [`docs/`](docs/):
1. **Game logic is terminal-agnostic** (`src/tino/engine/`):
   - Never import `curses` or handle raw keys inside `engine/`.
   - All mechanics, collision, and physics must be purely testable with standard `pytest`.
2. **UI is a thin presentation layer** (`src/tino/ui/`):
   - Only reads engine state and renders text/ASCII. Never mutates game rules directly.
3. **Storage uses clean abstractions** (`src/tino/storage/`):
   - Adhere to the `HighScoreStore` protocol so cloud stores can be plugged in seamlessly later.

---

## 🌿 Git & Branch Workflow

We follow standard GitHub Flow:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/tino.git
   cd tino
   ./scripts/setup.sh
   source .venv/bin/activate
   ```

2. **Create a feature branch**:
   Branch names should follow:
   - `feature/<module-name>-<short-description>` (e.g. `feature/engine-duck-mechanic`)
   - `fix/<bug-description>` (e.g. `fix/macos-terminal-resize`)
   - `docs/<doc-update>` (e.g. `docs/update-architecture`)

3. **Develop & Test**:
   - Write unit tests under `tests/unit/` for any new engine or storage logic.
   - Run tests: `./scripts/test.sh`
   - Run linter: `./scripts/lint.sh`

4. **Submit a Pull Request (PR)**:
   - Push your branch to GitHub.
   - Open a PR targeting `main`.
   - CI will automatically run tests and linting across macOS and Linux.

---

## 👥 Module Ownership & Task Distribution

See [docs/TEAM_TASKS.md](docs/TEAM_TASKS.md) for the active work distribution matrix and roadmap feature tracks.

### Major Subsystems:
- **Engine Core** (`src/tino/engine/`): State machines, collision, speed curves, entity math.
- **UI & Graphics** (`src/tino/ui/`): Terminal lifecycle, ASCII art sprites, color palettes, animations.
- **CLI & Controls** (`src/tino/cli.py`, `src/tino/config.py`): Command parsing, key remapping, custom configs.
- **Storage & Cloud** (`src/tino/storage/`): Local persistence, future remote/leaderboard sync.
- **Testing & Quality** (`tests/`, `.github/`): Integration suites, CI matrix, benchmark tests.
