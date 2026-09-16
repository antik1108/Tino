# 8. Testing

## 8.1 Strategy

Because engine logic is deliberately isolated from curses (see [Architecture §3.1](./03-architecture.md)), the majority of the test suite runs with no real terminal attached — plain `pytest`, fast, and CI-friendly.

| Layer | How it's tested |
|-------|-------------------|
| `engine/collision.py` | Pure unit tests — feed known positions, assert overlap/no-overlap. |
| `engine/entities.py` | Unit tests on jump trajectory math (position over successive ticks). |
| `engine/difficulty.py` | Unit tests asserting speed/spawn-rate as a function of elapsed time. |
| `engine/state.py` / `game.py` | Unit tests driving the state machine through legal and illegal transitions. |
| `storage/highscore.py` | Unit tests against a temp directory (via `tmp_path` fixture) — including missing-file and corrupt-file cases. |
| `config.py` | Unit tests for default merging and unknown-key handling. |
| `ui/*` | Thin integration checks only (e.g. renderer produces expected output for a given state) — not exhaustively unit tested, since it's a thin, mostly side-effecting layer. |

## 8.2 Structure

```
tests/
├── unit/
│   ├── test_collision.py
│   ├── test_entities.py
│   ├── test_difficulty.py
│   ├── test_state.py
│   ├── test_highscore.py
│   └── test_config.py
└── integration/
    └── test_app_wiring.py   # confirms app.py assembles engine + ui + storage correctly
```

## 8.3 Tooling

- **pytest** for the test runner.
- **Ruff** for linting and formatting (run in CI and via `scripts/lint.sh` locally).

## 8.4 CI

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and PR:
1. Set up Python 3.12+.
2. Install dependencies.
3. Run Ruff (lint + format check).
4. Run the full pytest suite.

A failing lint or test check blocks merge.
