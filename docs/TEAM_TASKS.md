# Team Work Distribution & Task Backlog

This document outlines how work is distributed across team members for GitHub issues, milestones, and pull requests based on the [Roadmap](10-roadmap.md) and [Architecture](03-architecture.md).

---

## 📋 Team Work Tracks

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TINO TEAM WORK TRACKS                           │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ Track A: Engine   │ Track B: UI & Art │ Track C: Infra, CLI & Storage  │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • Duck mechanic   │ • Pterodactyl art │ • Config editor CLI            │
│ • Obstacle types  │ • Day/Night theme │ • Remote leaderboard backend   │
│ • Score bonuses   │ • Frame animations│ • PyPI packaging & releases    │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

---

## 🎯 Task Breakdown for GitHub Issues

### Track A: Engine & Game Mechanics (Teammate 1 / Gameplay Lead)
- [ ] **Issue #1: Multi-Obstacle Spawning System (v2)**
  - *Location*: `src/tino/engine/entities.py`, `src/tino/engine/difficulty.py`
  - *Goal*: Add flying obstacles (e.g. birds/pterodactyls) at varying heights.
  - *Unit Tests*: `tests/unit/test_entities.py`
- [ ] **Issue #2: Duck / Crouch Mechanic (v2)**
  - *Location*: `src/tino/engine/entities.py`, `src/tino/engine/state.py`
  - *Goal*: Allow player to duck under flying obstacles, modifying hitbox height from 4 to 2.
  - *Unit Tests*: Verify crouched player bounding box avoids high obstacle.
- [ ] **Issue #3: Combo & Score Multipliers (v2)**
  - *Location*: `src/tino/engine/game.py`
  - *Goal*: Award bonus points for close-call obstacle dodges.

---

### Track B: UI, Terminal & Graphics (Teammate 2 / Frontend Lead)
- [ ] **Issue #4: Dynamic Day / Night Theme (v2)**
  - *Location*: `src/tino/ui/renderer.py`, `src/tino/ui/terminal.py`
  - *Goal*: Invert terminal colors every 500 score points to simulate day/night transitions like the original Dino game.
- [ ] **Issue #5: Expanded ASCII Sprite Library & Animations (v2)**
  - *Location*: `src/tino/ui/renderer.py`
  - *Goal*: Add 3-frame running animations, flying pterodactyl flapping wings, and ducking sprite.
- [ ] **Issue #6: Sound / Bell FX (v2 optional)**
  - *Location*: `src/tino/ui/renderer.py` (or new audio utility)
  - *Goal*: Use terminal bell (`\a` / `curses.beep()`) on reaching score milestones or game over (toggleable in config).

---

### Track C: Storage, CLI, Config & Distribution (Teammate 3 / Backend & DevOps Lead)
- [ ] **Issue #7: Interactive Key Rebinding CLI (v2)**
  - *Location*: `src/tino/cli.py`, `src/tino/config.py`
  - *Goal*: Add `tino config --rebind` command to let users set custom jump/duck keys interactively.
- [ ] **Issue #8: Remote Leaderboard Store Implementation (v3)**
  - *Location*: `src/tino/storage/highscore.py`
  - *Goal*: Implement `RemoteHighScoreStore(HighScoreStore)` to sync high scores to a REST API or Redis backend.
- [ ] **Issue #9: PyPI Automated Release Workflow (v3)**
  - *Location*: `.github/workflows/release.yml`, `pyproject.toml`
  - *Goal*: Add GitHub Action to build wheels and publish to PyPI on Git tag release.

---

## 🚀 How to Assign and Work
1. Pick a task from above or from the GitHub Issues tab.
2. Assign the issue to yourself on GitHub.
3. Create a feature branch: `git checkout -b feature/<issue-number>-<short-name>`.
4. Ensure all unit tests pass with `./scripts/test.sh`.
5. Open a Pull Request and tag your teammates for review!
