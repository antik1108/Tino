# 1. Overview

## What TINO is

TINO is a terminal-based endless runner in the spirit of Chrome's offline dinosaur game. You run it with:

```bash
tino
```

The player character auto-runs across the terminal and must jump over incoming obstacles. The game speeds up over time; the run ends the first time an obstacle is hit. The goal each run is to beat your own high score.

## Why terminal-based

No GUI framework, no browser, no external runtime — just Python and the terminal. This keeps the project:
- **Portable**: runs anywhere Python + a terminal exists (macOS, Linux).
- **Small in surface area**: the whole dependency footprint is the Python standard library plus dev tooling (pytest, Ruff). Nothing to compile, no rendering engine to fight.
- **A clean showcase of core CS/software-engineering fundamentals** — a real game loop, state management, and terminal I/O, without a framework doing the hard parts for you.

## Who it's for

- Primary: developers who live in a terminal and want a quick, satisfying break without leaving it.
- Secondary (project goal): a polished, real piece of software that demonstrates practical system design — not a toy script.

## Product goals

1. Smooth, responsive gameplay in a terminal (no visible flicker/lag on a normal machine).
2. Works identically whether launched from Bash or Zsh, on macOS or Linux.
3. High scores persist locally between runs.
4. Codebase stays maintainable as features are added — game logic isolated from terminal-specific code so either could change independently.
5. Installable and runnable by someone who isn't the author, with minimal setup friction.

## Non-goals (for now)

- No GUI/web version.
- No networked multiplayer.
- No Windows support in v1 (curses' Windows story is inconsistent; revisit later if needed).
