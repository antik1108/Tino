# 5. Terminal Behavior

## 5.1 Why `curses`

`curses` is the standard-library terminal UI toolkit on macOS and Linux, gives direct control over cursor position and screen buffering, and handles a lot of terminal-capability differences internally. It's the natural choice for "no external UI dependency" — no ncurses-alternative package needed.

## 5.2 Startup / teardown

`ui/terminal.py` wraps `curses.wrapper()` (or an equivalent explicit init/`try`/`finally`), which guarantees:
- Raw/cbreak mode and non-blocking input are set up on start.
- The terminal is always restored to its normal (cooked) state on exit — including on a crash or `Ctrl+C` — so the user's shell is never left in a broken state. This directly satisfies NFR-2 in the requirements.

## 5.3 Shell independence (Bash vs Zsh)

TINO doesn't do anything shell-specific — the game itself is a compiled/installed Python entry point (`tino`), not a shell script, so it behaves identically regardless of which shell launched it. The only shell-touching pieces are the dev-only scripts in `scripts/` (setup/lint/test), which are plain POSIX-compatible Bash and don't affect the shipped game.

## 5.4 Terminal size / resize

- On start, TINO reads the current terminal dimensions and lays out the play area to fit.
- If the terminal is resized mid-run, `ui/terminal.py` detects it (via curses' resize signal handling) and the renderer adapts on the next frame rather than crashing or drawing out of bounds.
- If the terminal is too small to render a playable area, TINO shows a clear message asking the user to resize, rather than rendering garbled output.

## 5.5 Input handling

- Input is read non-blocking each frame (`ui/input.py`), so a held or absent keypress never stalls the game loop.
- Keycodes are mapped to abstract actions (`JUMP`, `QUIT`, `RESTART`) at this layer — the engine only ever sees actions, never raw keys, which is what keeps the engine terminal-agnostic (see [Architecture §3.1](./03-architecture.md)).

## 5.6 macOS vs Linux differences

Both are POSIX terminals with curses available in the Python standard library, so no OS-specific branching is expected. The only practical difference to watch for during implementation is default terminal emulator quirks (e.g. macOS Terminal.app vs iTerm2 vs common Linux emulators like GNOME Terminal) around color support and key-escape-sequence timing — handled generically by curses rather than special-cased per OS.
