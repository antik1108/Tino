# 9. Tech Stack

Only what's actually used in TINO, and why each was chosen.

| Tool | Used for | Why this, specifically |
|------|----------|--------------------------|
| **Python 3.12+** | The entire application | Standard library alone covers everything needed (terminal UI, JSON, paths) — no external runtime required, matching the "no GUI framework/runtime" goal in the overview. |
| **curses** | Terminal rendering & raw input | Standard-library terminal toolkit on macOS/Linux; handles low-level terminal capability differences without an extra dependency. |
| **argparse** | CLI (`tino`, `tino score`, `tino reset-score`) | Standard library, sufficient for a small, fixed set of commands — no need for a heavier CLI framework. |
| **JSON + pathlib** | Local persistence (high score, config) | Human-readable, no schema/migration tooling needed at this scale; `pathlib` gives cross-platform (macOS/Linux) file path handling. |
| **pytest** | Testing | De facto standard Python test runner; fixtures (e.g. `tmp_path`) are a natural fit for testing the storage layer in isolation. |
| **Ruff** | Linting + formatting | Single fast tool covering both lint and format, replacing the need for separate linter + formatter + import-sorter. |
| **Git + GitHub** | Version control, collaboration | Standard choice; also hosts CI and (later) releases. |
| **GitHub Actions** | CI | Runs lint + tests on every push, native to GitHub, no separate CI service needed. |
| **pyproject.toml** | Project/packaging configuration | Modern standard single-file config for build metadata, dependencies, and tool settings (Ruff, pytest) — avoids scattering config across multiple files. |
| **Bash** | Dev/setup scripts only (`scripts/`) | Convenience wrappers for contributors (setup/lint/test) — not part of the shipped game, so it doesn't affect shell independence (see [Terminal Behavior §5.3](./05-terminal-behavior.md)). |

**Deliberately not used (for now):** any third-party UI/game framework, a database, a web framework, or a packaging step beyond `pyproject.toml` — none are justified by v1's actual scope. PyPI publishing is planned (see [Roadmap](./10-roadmap.md)) but isn't a v1 requirement.
