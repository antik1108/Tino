"""Terminal initialization, safe teardown, and size monitoring."""

import curses
from collections.abc import Generator
from contextlib import contextmanager

MIN_TERMINAL_WIDTH = 60
MIN_TERMINAL_HEIGHT = 16


class Terminal:
    """Manages curses window lifecycle and screen properties."""

    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self._setup_curses()

    def _setup_curses(self) -> None:
        """Configure curses for raw, non-blocking, hidden-cursor operation."""
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)  # non-blocking getch
        try:
            curses.curs_set(0)  # hide cursor
        except curses.error:
            pass

        # Try color initialization if supported
        if curses.has_colors():
            try:
                curses.start_color()
                curses.use_default_colors()
                # Define color pairs
                curses.init_pair(1, curses.COLOR_GREEN, -1)  # Dino / obstacles
                curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Scores & highlights
                curses.init_pair(3, curses.COLOR_RED, -1)  # Game Over / danger
                curses.init_pair(4, curses.COLOR_CYAN, -1)  # Title & borders
            except curses.error:
                pass

    @property
    def dimensions(self) -> tuple[int, int]:
        """Return (height, width) of the current terminal screen."""
        try:
            h, w = self.stdscr.getmaxyx()
            return h, w
        except curses.error:
            return 24, 80

    def is_size_adequate(self) -> bool:
        """Check if the current terminal meets the minimum playable size."""
        h, w = self.dimensions
        return h >= MIN_TERMINAL_HEIGHT and w >= MIN_TERMINAL_WIDTH

    def clear(self) -> None:
        """Clear screen buffer."""
        try:
            self.stdscr.erase()
        except curses.error:
            pass

    def refresh(self) -> None:
        """Flush changes to physical terminal."""
        try:
            self.stdscr.refresh()
        except curses.error:
            pass


@contextmanager
def terminal_session() -> Generator[Terminal, None, None]:
    """Context manager ensuring safe terminal initialization and clean restoration."""
    stdscr = curses.initscr()
    terminal = Terminal(stdscr)
    try:
        yield terminal
    finally:
        # Guaranteed cleanup even on exception or Ctrl+C
        try:
            stdscr.keypad(False)
            curses.nocbreak()
            curses.echo()
            try:
                curses.curs_set(1)
            except curses.error:
                pass
            curses.endwin()
        except Exception:
            pass
