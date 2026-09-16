"""Screen renderer for TINO engine state."""

import curses
from tino.engine.game import Game
from tino.engine.state import GameState
from tino.ui.terminal import Terminal

# ASCII Sprites for Player (Height = 4, Width = 5)
SPRITE_DINO_RUN_1 = [
    "  ■_ ",
    " <(o)",
    " /|\\ ",
    " / \\ ",
]

SPRITE_DINO_RUN_2 = [
    "  ■_ ",
    " <(o)",
    " /|\\ ",
    "  |\\ ",
]

SPRITE_DINO_JUMP = [
    "  ■_ ",
    " <(^)",
    " /|\\ ",
    " /_  ",
]

SPRITE_DINO_DEAD = [
    "  ■_ ",
    " <(x)",
    " /|\\ ",
    " _/\\_",
]

# Obstacle Sprite (Height = 3, Width = 3)
SPRITE_CACTUS = [
    " | #",
    "###|",
    " |  ",
]


class Renderer:
    """Draws current engine state onto the curses terminal window."""

    def __init__(self, terminal: Terminal) -> None:
        self.terminal = terminal
        self._ground_scroll_offset = 0.0

    def safe_addstr(
        self,
        y: int,
        x: int,
        text: str,
        attr: int = 0,
    ) -> None:
        """Draw string safely at (y, x) with boundary clipping and error suppression."""
        h, w = self.terminal.dimensions
        if y < 0 or y >= h or x >= w:
            return

        # Clip text if it overflows width
        if x < 0:
            text = text[-x:]
            x = 0
        if x + len(text) >= w:
            text = text[: max(0, w - x - 1)]

        if text:
            try:
                self.terminal.stdscr.addstr(y, x, text, attr)
            except curses.error:
                pass

    def render(self, game: Game) -> None:
        """Render frame according to the game state."""
        self.terminal.clear()

        if not self.terminal.is_size_adequate():
            self._render_size_warning()
            self.terminal.refresh()
            return

        # Update world width in game engine to match current terminal width
        h, w = self.terminal.dimensions
        game.world_width = float(w)

        if game.state == GameState.MENU:
            self._render_menu(game)
        elif game.state == GameState.PLAYING:
            self._render_playing(game)
        elif game.state == GameState.GAME_OVER:
            self._render_playing(game)
            self._render_game_over(game)

        self.terminal.refresh()

    def _render_size_warning(self) -> None:
        """Display notice when window is smaller than required bounds."""
        h, w = self.terminal.dimensions
        msg = f"Terminal too small ({w}x{h})."
        hint = "Please enlarge your terminal window (min 60x16)."
        self.safe_addstr(h // 2 - 1, max(0, (w - len(msg)) // 2), msg, curses.A_BOLD)
        self.safe_addstr(h // 2 + 1, max(0, (w - len(hint)) // 2), hint)

    def _render_menu(self, game: Game) -> None:
        """Render the start menu overlay."""
        h, w = self.terminal.dimensions
        center_x = w // 2
        center_y = h // 2

        title = [
            "  _____ _____ _   _  ____  ",
            " |_   _|_   _| \\ | |/ __ \\ ",
            "   | |   | | |  \\| | |  | |",
            "   | |   | | | . ` | |  | |",
            "   |_|  |___|_|\\_\\_|\\____/ ",
        ]

        # Draw ASCII Title Banner
        start_y = max(2, center_y - 6)
        for i, line in enumerate(title):
            self.safe_addstr(
                start_y + i,
                center_x - len(line) // 2,
                line,
                curses.color_pair(4) | curses.A_BOLD,
            )

        tagline = "TERMINAL DINO ENDLESS RUNNER"
        self.safe_addstr(
            start_y + len(title) + 1,
            center_x - len(tagline) // 2,
            tagline,
            curses.A_DIM,
        )

        hi_text = f"HIGH SCORE: {game.high_score:05d}"
        self.safe_addstr(
            start_y + len(title) + 3,
            center_x - len(hi_text) // 2,
            hi_text,
            curses.color_pair(2) | curses.A_BOLD,
        )

        prompt = "▶  PRESS SPACE / ENTER TO START  ◀"
        self.safe_addstr(
            start_y + len(title) + 5,
            center_x - len(prompt) // 2,
            prompt,
            curses.color_pair(1) | curses.A_BOLD,
        )

        quit_hint = "Press [Q] to quit at any time"
        self.safe_addstr(
            h - 2,
            center_x - len(quit_hint) // 2,
            quit_hint,
            curses.A_DIM,
        )

    def _render_playing(self, game: Game) -> None:
        """Draw active gameplay screen: HUD, Dino, obstacles, and scrolling ground."""
        h, w = self.terminal.dimensions
        ground_y = h - 4

        # 1. Draw HUD
        hud_title = " TINO "
        score_text = f"SCORE: {game.score:05d}   HI: {game.high_score:05d}"
        speed_factor = game.current_speed / game.config.initial_speed
        speed_text = f"SPD: {speed_factor:.1f}x "

        self.safe_addstr(1, 2, hud_title, curses.color_pair(4) | curses.A_BOLD)
        self.safe_addstr(1, w - len(score_text) - len(speed_text) - 4, score_text, curses.color_pair(2) | curses.A_BOLD)
        self.safe_addstr(1, w - len(speed_text) - 2, speed_text, curses.A_DIM)

        # 2. Draw Ground Line & Texture
        self._ground_scroll_offset = (self._ground_scroll_offset + game.current_speed * 0.05) % 20
        ground_pattern = "___.__.__...____.___"
        full_ground = (ground_pattern * ((w // len(ground_pattern)) + 2))
        offset_idx = int(self._ground_scroll_offset) % len(ground_pattern)
        visible_ground = full_ground[offset_idx : offset_idx + w]

        self.safe_addstr(ground_y, 0, "=" * w, curses.A_DIM)
        self.safe_addstr(ground_y + 1, 0, visible_ground, curses.A_DIM)

        # 3. Draw Player
        player = game.player
        player_x = int(player.x)
        # Ground coordinate in terminal is (ground_y - height - player.y)
        player_y = int(ground_y - player.height - player.y)

        # Select sprite based on state and running animation
        if game.state == GameState.GAME_OVER:
            sprite = SPRITE_DINO_DEAD
        elif not player.is_grounded:
            sprite = SPRITE_DINO_JUMP
        else:
            anim_frame = int(game.elapsed_time * 10) % 2
            sprite = SPRITE_DINO_RUN_1 if anim_frame == 0 else SPRITE_DINO_RUN_2

        for row_idx, line in enumerate(sprite):
            self.safe_addstr(
                player_y + row_idx,
                player_x,
                line,
                curses.color_pair(1) | curses.A_BOLD,
            )

        # 4. Draw Obstacles
        for obs in game.obstacles:
            obs_x = int(obs.x)
            obs_y = int(ground_y - obs.height - obs.y)
            for row_idx, line in enumerate(SPRITE_CACTUS):
                self.safe_addstr(
                    obs_y + row_idx,
                    obs_x,
                    line,
                    curses.color_pair(3) | curses.A_BOLD,
                )

    def _render_game_over(self, game: Game) -> None:
        """Render Game Over overlay dialog."""
        h, w = self.terminal.dimensions
        center_x = w // 2
        box_y = max(3, h // 2 - 4)

        box_width = 44
        box_left = center_x - box_width // 2

        # Draw dialog box background border
        border_top = "┌" + "─" * (box_width - 2) + "┐"
        border_mid = "│" + " " * (box_width - 2) + "│"
        border_bot = "└" + "─" * (box_width - 2) + "┘"

        self.safe_addstr(box_y, box_left, border_top, curses.color_pair(3))
        for r in range(1, 8):
            self.safe_addstr(box_y + r, box_left, border_mid, curses.color_pair(3))
        self.safe_addstr(box_y + 8, box_left, border_bot, curses.color_pair(3))

        # Game Over Banner
        go_title = "★  G A M E   O V E R  ★"
        self.safe_addstr(
            box_y + 2,
            center_x - len(go_title) // 2,
            go_title,
            curses.color_pair(3) | curses.A_BOLD,
        )

        # High Score notice
        if game.is_new_high_score:
            record_str = f"★ NEW HIGH SCORE: {game.score:05d}! ★"
            self.safe_addstr(
                box_y + 4,
                center_x - len(record_str) // 2,
                record_str,
                curses.color_pair(2) | curses.A_BOLD,
            )
        else:
            final_str = f"Final Score: {game.score:05d}   |   Best: {game.high_score:05d}"
            self.safe_addstr(
                box_y + 4,
                center_x - len(final_str) // 2,
                final_str,
                curses.A_BOLD,
            )

        # Restart Instructions
        controls = "[R] Restart    |    [Q] Quit"
        self.safe_addstr(
            box_y + 6,
            center_x - len(controls) // 2,
            controls,
            curses.color_pair(1) | curses.A_BOLD,
        )
