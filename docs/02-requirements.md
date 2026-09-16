# 2. Requirements (PRD)

## 2.1 Functional requirements — v1

| ID | Requirement |
|----|-------------|
| FR-1 | Running `tino` launches the game directly into a start screen. |
| FR-2 | Player can start a run, jump over obstacles, and the run ends on collision. |
| FR-3 | A single obstacle type exists in v1 (ground-level, e.g. cactus-style block). |
| FR-4 | Game speed increases progressively the longer a run lasts. |
| FR-5 | Score increases automatically for as long as the player survives. |
| FR-6 | On game over, the current run's score is compared against the stored high score; if higher, it's saved. |
| FR-7 | Player can restart a run without relaunching the program (e.g. press a key at the game-over screen). |
| FR-8 | Player can quit cleanly at any point (e.g. `q` or `Ctrl+C`), and the terminal is restored to its normal state on exit. |
| FR-9 | CLI supports at least: running the game, viewing the current high score, and resetting the high score. |
| FR-10 | The game behaves identically when launched from Bash or Zsh, on macOS or Linux. |

## 2.2 Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | **Performance**: consistent frame pacing — no perceptible stutter on a typical laptop. |
| NFR-2 | **Resilience**: an unhandled error must not leave the user's terminal in a broken/raw state. |
| NFR-3 | **Portability**: standard library + the listed dependencies only; no OS-specific code paths beyond what curses already abstracts. |
| NFR-4 | **Maintainability**: game logic (rules, state, scoring) must be testable without a real terminal attached. |
| NFR-5 | **Test coverage**: core engine logic (collision, scoring, difficulty, state transitions) covered by unit tests; UI layer covered where practical. |
| NFR-6 | **Config**: sensible defaults with no required setup; an optional config file can override behavior (e.g. key bindings) later. |

## 2.3 In scope for v1

- Single-player, single obstacle type, progressive difficulty, local high score, start/playing/game-over flow, CLI with run/show-score/reset-score.

## 2.4 Explicitly out of scope for v1 (see [Roadmap](./10-roadmap.md))

- Multiple obstacle types / obstacle variety
- Duck/crouch mechanic
- Sound
- Themes/skins
- Cloud-synced high scores
- PyPI packaging (planned, not v1)
- Windows support

## 2.5 Success criteria

- A new user can clone the repo, follow the README, and be playing within a couple of minutes.
- The game runs without visual glitches on both macOS Terminal/iTerm2 and common Linux terminal emulators.
- Core engine test suite passes in CI on every push.
