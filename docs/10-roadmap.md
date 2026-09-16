# 10. Roadmap

## v1 — Core game (current scope)
- Single obstacle type, jump-only mechanic, progressive difficulty.
- Local JSON high score, optional local config.
- `tino` / `tino score` / `tino reset-score` CLI.
- Full unit test coverage on engine + storage, CI on every push.
- Install via clone + run locally.

## v2 — Depth & polish
- Additional obstacle types with varied spawn patterns.
- Duck/crouch mechanic (for overhead obstacles).
- Visual polish (color, simple animation frames within curses' capabilities).
- Config-driven key rebinding exposed to the player (not just editable JSON).

## v3 — Distribution & reach
- Publish to PyPI (`pip install tino`) — the packaging groundwork (`pyproject.toml`) is already in place from v1, so this is primarily a release-process step, not a rearchitecture.
- Optional cloud/remote high-score sync, implemented as a second `HighScoreStore` implementation (see [Architecture §3.7](./03-architecture.md)) — no engine changes required.
- Evaluate Windows support if there's demand (would require revisiting the curses dependency, likely via `windows-curses`).

## Explicitly not planned
- Networked multiplayer.
- A GUI/web version — if that's ever wanted, it's a different project sharing the engine, not a pivot of TINO itself.
