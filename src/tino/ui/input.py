"""Non-blocking keyboard input reader and action mapper."""

import curses

from tino.config import Config
from tino.engine.state import Action

# Regular Enter (newline / carriage-return) and keypad Enter
_ENTER_KEYS = (10, 13, curses.KEY_ENTER)


class InputHandler:
    """Reads curses key events non-blockingly and maps to high-level engine Actions."""

    def __init__(self, stdscr: curses.window, config: Config | None = None) -> None:
        self.stdscr = stdscr
        self.config = config or Config()

    def get_action(self) -> Action:
        """Poll the next keypress non-blockingly and translate to an Action."""
        try:
            key = self.stdscr.getch()
        except curses.error:
            return Action.NONE

        if key == -1:
            return Action.NONE

        # --- Fast-path: Ctrl+C (ASCII 3) always quits immediately ---
        if key == 3:
            return Action.QUIT

        # --- Normalise raw keycode → canonical string ---
        if key == curses.KEY_UP:
            key_str = "KEY_UP"
        elif key == curses.KEY_RESIZE:
            # Terminal resize signal — not a user action, ignore it
            return Action.NONE
        elif key in (32, ord(" ")):
            # Space bar — stored as both " " and "space" in defaults;
            # normalise to "space" so either spelling in config works.
            key_str = "space"
        elif key in _ENTER_KEYS:
            # Enter / Return acts as both START (menu) and JUMP (playing).
            # Return the higher-priority action directly; no further matching needed.
            return Action.JUMP
        else:
            try:
                key_str = chr(key)
            except (ValueError, OverflowError):
                key_str = str(key)

        bindings = self.config.keybindings

        # Quit bindings (case-insensitive)
        quit_lower = {k.lower() for k in bindings.quit}
        if key_str in bindings.quit or key_str.lower() in quit_lower:
            return Action.QUIT

        # Jump bindings — also accept bare " " alongside "space"
        jump_set = set(bindings.jump)
        if key_str in jump_set or (key_str == "space" and " " in jump_set):
            return Action.JUMP

        # Restart bindings (case-insensitive)
        restart_lower = {k.lower() for k in bindings.restart}
        if key_str in bindings.restart or key_str.lower() in restart_lower:
            return Action.RESTART

        # Any other printable key triggers START (used on the MENU screen).
        if key_str.isprintable():
            return Action.START

        return Action.NONE
