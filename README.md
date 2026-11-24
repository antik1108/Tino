# TINO — Terminal Dino Endless Runner

TINO is a Python terminal game inspired by Chrome's offline dinosaur game. The runner stays near the left edge while obstacles move toward it. Jump over them, survive as long as possible, and try to beat your locally saved high score.

The game uses Python's standard library, including `curses` for terminal input and drawing. Its game rules are separate from the terminal code, so most behavior can be checked without opening a terminal window.

## Requirements and setup

- Python 3.12 or newer
- macOS or Linux and an interactive terminal of at least 60 columns by 16 rows
- Bash for the convenience scripts

From the repository root:

```bash
./scripts/setup.sh
source .venv/bin/activate
tino
```

The setup script creates `.venv` and installs the project in editable mode with development tools. Alternatively:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
tino
```

An editable install makes source changes available without reinstalling. Runtime dependencies are provided by Python; pytest and Ruff are development dependencies. Windows is not currently supported.

## Controls and commands

| Input | Action |
| --- | --- |
| Space, Up arrow, `w`, or Enter | Start or jump |
| `r` | Restart after game over |
| `q` or Ctrl+C | Quit |
| Other printable key | Start from the menu; also restarts after game over |

While playing, a jump can only start when the player is on the ground. A key press on the menu starts the run; it does not also make the player jump.

```bash
tino                       # Start the game
tino score                 # Print the saved high score
tino reset-score           # Ask before resetting the score
tino reset-score --force   # Reset without asking
tino --version             # Print the version
tino --help                # Show command help
```

## How the game runs

The `tino` entry point in `pyproject.toml` calls `tino.cli.main()`. It parses the command and either runs a score command or calls `run_app()` in `app.py`. The application loads settings and a score store, creates a `Game`, and opens a terminal session.

The application repeats this cycle until the player quits:

1. Measure `dt`, the time since the previous update, using `time.perf_counter()`. A single step is capped at 0.1 seconds to limit jumps after a long stall.
2. Read a key without waiting and translate it into an action such as `JUMP` or `QUIT`.
3. Pass the action to the game and call `Game.tick(dt)` to advance the rules.
4. Draw the current screen and wait for the remainder of the target frame interval, if any.

The default target is 30 updates per second. Movement uses elapsed time, rather than assuming every update takes exactly the same time. Because long steps are capped, game time can fall behind real time during a stall.

### Input, jumping, and drawing

`InputHandler.get_action()` maps the Up arrow, Space, and other configured keys to game actions. In the playing state, `Game.handle_action()` calls `Player.jump()`. If the player is grounded, it sets vertical velocity to 18 game units per second. Each update then applies:

```python
y += y_velocity * dt
y_velocity -= gravity * dt  # gravity is 42 units per second squared
```

The player rises, slows down, falls, and is reset to ground level with zero velocity upon landing. At consistent 30 updates per second, the peak is approximately 4.16 game units and the full jump lasts about 0.9 seconds. The exact result depends on update timing. The renderer converts the floating-point height to a terminal row; at that peak the character appears about five rows above its ground position.

`curses` manages the screen and keyboard. The terminal layer hides typed keys and the cursor, enables immediate key reads, and restores terminal settings when the session exits. The renderer clears and redraws the menu, play area, or game-over screen and clips text at screen edges. It shows a warning when the window is too small. The game continues updating while that warning is displayed, so enlarge the terminal before starting or resuming play.

### Rules, difficulty, and collision

The game has three states: `MENU`, `PLAYING`, and `GAME_OVER`. Starting or restarting resets the player, obstacles, score, and timers. During play, `Game.tick()`:

1. Increases elapsed time and sets the score to `int(elapsed_time * 10)`.
2. Calculates speed as `min(65, 25 + elapsed_time * 0.5)` with the default settings.
3. Updates the player and moves obstacles left by `speed * dt`; obstacles fully past the left edge are removed.
4. Spawns a cactus at the right edge after a random interval. Initially this is between 1.2 and 2.8 seconds; the interval shrinks as speed rises, with lower bounds in the calculation.
5. Checks whether the player's and each obstacle's rectangles overlap. Each rectangle is inset by 0.4 units for the check, making edge grazes more forgiving.

On collision, the run ends. A score greater than the saved high score is saved. The speed reaches its default maximum after 80 seconds. Obstacle spacing and jump behavior should still be assessed through playtesting; the interval bounds alone do not prove every sequence is fair.

## Configuration and saved data

Both `config.json` and `highscore.json` live in the TINO data directory:

| System | Directory |
| --- | --- |
| macOS | `~/Library/Application Support/tino` |
| Linux | `$XDG_DATA_HOME/tino`, or `~/.local/share/tino` if unset |
| Other systems | `~/.tino` fallback; gameplay support is not guaranteed |

Configuration is optional. For example:

```json
{
  "target_fps": 30,
  "keybindings": {
    "jump": ["space", "KEY_UP", "w"],
    "quit": ["q", "Q"],
    "restart": ["r", "R"]
  }
}
```

Each binding accepts a string or a list. A supplied binding replaces that action's defaults. Enter remains a jump/start key and Ctrl+C remains a quit action. `target_fps` must be a positive integer; the loop uses at least 10 updates per second. Speed and obstacle timing defaults are defined in `Config` but are not currently loaded from JSON. Unknown settings are ignored and missing or malformed configuration falls back to defaults.

The high-score file contains `high_score` and an `updated_at` timestamp. A missing file, malformed JSON, or invalid score value normally reads as zero. Save errors are silently ignored, so a score shown during a session may not persist if the file cannot be written. Valid JSON with an unexpected top-level type can also cause a read error; this is a known limitation.

## Code map

| Path | Responsibility |
| --- | --- |
| `src/tino/cli.py` | Parse commands and dispatch to the game or score operations |
| `src/tino/app.py` | Assemble components and run the update cycle |
| `src/tino/config.py` | Defaults and optional configuration loading |
| `src/tino/engine/game.py` | Actions, run state, scoring, spawning, and updates |
| `src/tino/engine/entities.py` | Player jump and obstacle movement |
| `src/tino/engine/collision.py` | Rectangle overlap check |
| `src/tino/engine/difficulty.py` | Speed and randomized spawn intervals |
| `src/tino/engine/state.py` | Game states, actions, and allowed transitions |
| `src/tino/ui/` | Terminal setup, keyboard input, and drawing |
| `src/tino/storage/` | Data paths and JSON high-score storage |
| `tests/` | Unit tests and command/component integration checks |
| `scripts/` | Setup, test, and lint helpers |

`HighScoreStore` describes the load, save, and reset operations the game expects; `JSONHighScoreStore` supplies the local implementation. The game can accept another store with those operations. The transition helper lists permitted state changes, although the current start and game-over methods assign states directly.

## Development and checks

```bash
./scripts/test.sh       # Run unit and integration tests
./scripts/lint.sh       # Run Ruff lint and format checks
```

The tests cover movement, collision, difficulty, state behavior, configuration, score storage, and some command wiring. Terminal rendering and real terminal behavior have less coverage and benefit from manual checks. GitHub Actions is configured to run lint and tests on Ubuntu and macOS with Python 3.12 and 3.13 for pushes and pull requests targeting the configured branches.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance and [docs/](docs/) for design notes and plans. Some design documents describe intended behavior and may lag the implementation; use the source as the authority for current behavior.

## License

MIT. See [LICENSE](LICENSE).
