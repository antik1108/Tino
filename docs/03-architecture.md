# 3. Architecture

## 3.1 Guiding principle

Game logic (rules, state, scoring, collision) must not know that a terminal exists. The terminal/curses layer is just one possible "renderer + input source" sitting on top of a plain Python engine. This is what makes the engine unit-testable without a real terminal, and lets the rendering layer change later without touching game rules.

## 3.2 Project structure

```
tino/
├── src/tino/
│   ├── __init__.py
│   ├── cli.py              # argparse entry point — parses args, dispatches to a command
│   ├── app.py               # wires everything together: config → engine → UI → run loop
│   ├── config.py             # loads defaults, merges optional user config
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── game.py            # Game class: owns the state machine + drives the game loop
│   │   ├── state.py            # GameState enum + transition rules (MENU, PLAYING, GAME_OVER)
│   │   ├── entities.py          # Player, Obstacle — includes jump/gravity movement logic
│   │   ├── collision.py          # pure collision-detection functions
│   │   └── difficulty.py          # speed/spawn-rate progression as a function of elapsed time
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── terminal.py           # curses init/teardown, screen size, resize handling
│   │   ├── renderer.py            # draws engine state to the screen — no game logic here
│   │   └── input.py                # non-blocking key reads, maps keys → engine actions
│   └── storage/
│       ├── __init__.py
│       ├── highscore.py            # HighScoreStore interface + JSONHighScoreStore
│       └── paths.py                 # resolves the OS-appropriate data directory
├── tests/
│   ├── unit/                        # engine, storage, config — no terminal required
│   └── integration/                  # thin checks that the pieces wire together correctly
├── scripts/
│   ├── setup.sh                      # create venv, install deps
│   ├── lint.sh                        # run Ruff
│   └── test.sh                         # run pytest
├── docs/                               # this folder
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

## 3.3 Module responsibilities

| Module | Owns | Does NOT know about |
|--------|------|----------------------|
| `engine/game.py` | The state machine, the game loop tick, coordinating entities/collision/difficulty | curses, terminal size, keycodes |
| `engine/entities.py` | Player and Obstacle position/movement (including jump arc — see 3.5) | Rendering, input |
| `engine/collision.py` | Whether two entities overlap | Everything else — pure functions in, booleans out |
| `engine/difficulty.py` | Mapping elapsed time → current speed | Rendering, storage |
| `ui/terminal.py` | Starting/stopping curses safely, terminal size | Game rules |
| `ui/renderer.py` | Drawing a given engine state to the screen | Game rules — it only reads state, never mutates it |
| `ui/input.py` | Reading a keypress and mapping it to an action (`JUMP`, `QUIT`, `RESTART`) | What the action does |
| `storage/highscore.py` | Reading/writing the high score | The engine — the engine calls it, not the reverse |
| `cli.py` | Parsing `tino` command-line arguments | Game internals — it just starts `app.py` with the right options |

## 3.4 The game loop

A single fixed-interval loop, driven from `app.py`:

1. Read input (non-blocking) → translate to an action.
2. Advance engine state by one tick (move entities, check collisions, update difficulty/score).
3. Render the current state.
4. Sleep for the remainder of the frame interval.

This is a standard **game loop** pattern — chosen because it's the simplest correct way to get consistent pacing in a terminal, and every other design (event-driven redraw, for instance) adds complexity without benefit for a single-screen game like this.

## 3.5 Why no separate "Physics" module

A full physics module implies general simulation (multiple bodies, forces, constraints). TINO has exactly one moving vertical trajectory: the player's jump (a fixed initial velocity plus constant gravity, each tick). That's a few lines of arithmetic, not a subsystem — so it lives directly in `entities.py` next to the `Player` it belongs to. If TINO ever needs real physics (it won't for a dino runner), this is the seam where it would be extracted.

## 3.6 State machine

```
MENU ──(start)──> PLAYING ──(collision)──> GAME_OVER
  ^                                             │
  └─────────────────(restart)───────────────────┘
```

Justified because the game genuinely has distinct modes with different valid inputs and different rendering — a raw boolean ("is playing?") wouldn't cleanly express "just game-over, waiting for restart" vs "actively playing." `engine/state.py` defines the enum and the only legal transitions between them; `game.py` is the sole place that triggers a transition.

## 3.7 Storage design (for future cloud sync)

`storage/highscore.py` defines a small interface:

```python
class HighScoreStore(Protocol):
    def load(self) -> int: ...
    def save(self, score: int) -> None: ...
```

`JSONHighScoreStore` is the only implementation in v1, backed by a JSON file under a per-user data directory (see [Data Model](./07-data-model.md)). The engine depends only on the interface. If a remote/cloud store is added later, it's a new class implementing the same two methods — no changes needed anywhere else. This is intentionally the smallest possible abstraction that satisfies "local now, swappable later" — not a general plugin framework.

## 3.8 Error handling

- Terminal setup/teardown (`ui/terminal.py`) uses `try/finally` so the terminal is always restored to a normal state, even on an unhandled exception or `Ctrl+C`.
- Storage reads/writes are wrapped narrowly: a missing or corrupt high-score file is treated as "no high score yet" rather than crashing the game.
- The CLI validates arguments up front (via `argparse`) and fails with a clear message rather than surfacing a stack trace.

## 3.9 Configuration

`config.py` defines defaults in code (frame rate, initial speed, key bindings) and optionally merges a user config file if one exists (see [Data Model](./07-data-model.md)). No config file is required to run the game — this keeps FR (no required setup) satisfied while leaving room to customize later.
