# 4. Game Design

## 4.1 Core loop

Player auto-runs left to right (visually, the world scrolls right to left toward a stationary player). Obstacles spawn ahead and move toward the player. Player jumps to avoid them. Surviving longer increases both speed and score. One collision ends the run.

## 4.2 Controls

| Key | Action |
|-----|--------|
| `Space` / `↑` | Jump |
| `q` / `Ctrl+C` | Quit |
| `r` | Restart (only on game-over screen) |

Exact bindings live in config (see [Data Model](./07-data-model.md)) so they're changeable without touching code.

## 4.3 Player

- Fixed horizontal position on screen; only vertical movement (jump).
- Jump is a fixed-height arc: triggered by one key press, cannot be extended mid-air (no "hold to jump higher" in v1 — keeps input handling simple and predictable).
- Cannot jump again until landed (no double-jump in v1).

## 4.4 Obstacles — v1

- **Single type**: one ground-level obstacle (e.g. a cactus-style block), per your scope decision. Additional types are a v2 item (see [Roadmap](./10-roadmap.md)) and are designed for from the start (obstacles are a list of typed entities, not a hardcoded single object) so adding a second type later doesn't require restructuring.
- Spawn at a random-but-bounded interval so gaps are never impossible to clear.

## 4.5 Difficulty curve

- Game speed starts at a fixed base value and increases smoothly with elapsed survival time (not in sudden steps), handled by `engine/difficulty.py`.
- Obstacle spawn interval scales down slightly as speed increases, keeping challenge consistent rather than just "faster but same gaps."
- Exact curve (formula/constants) is a tunable value, not fixed in this doc — expect it to be adjusted by playtesting during implementation.

## 4.6 Scoring

- Score increases automatically over time survived (not from any explicit player action).
- On game over, score is compared to the stored high score; the higher value is kept.

## 4.7 Screens

- **Start (MENU)**: game title, high score, "press any key to start."
- **Playing**: the runner, current score shown live.
- **Game Over**: final score, high score (with a "new high score!" indicator if beaten), restart/quit prompt.

## 4.8 What's deliberately left out of v1

Duck/crouch, multiple obstacle types, sound, and themes are all real, natural extensions — they're deferred so v1 stays a small, complete, well-tested loop rather than a half-finished larger scope. See [Roadmap](./10-roadmap.md).
