"""Non-blocking keyboard input reader and action mapper."""

import curses

from tino.config import Config
from tino.engine.state import Action


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

        # Convert keycode to string representation
        key_str = ""
        if key in (curses.KEY_UP, 259):
            key_str = "KEY_UP"
        elif key in (32, ord(" ")):
            key_str = "space"
        elif key in (3, ord("q"), ord("Q")):
            # Ctrl+C is ascii 3
            if key == 3:
                return Action.QUIT
            key_str = chr(key)
        else:
            try:
                key_str = chr(key)
            except (ValueError, OverflowError):
                key_str = str(key)

        # Match against keybindings
        bindings = self.config.keybindings

        if key_str in bindings.quit or key_str.lower() in [k.lower() for k in bindings.quit]:
            return Action.QUIT

        if key_str in bindings.jump or (key_str == " " and "space" in bindings.jump):
            return Action.JUMP

        if key_str in bindings.restart or key_str.lower() in [k.lower() for k in bindings.restart]:
            return Action.RESTART

        # Any key in menu can start
        if key_str.isprintable() or key in (curses.KEY_ENTER, 10, 13):
            return Action.START

        return Action.NONE
