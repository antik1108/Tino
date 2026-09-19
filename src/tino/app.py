"""Main application entry point orchestrating game loop and UI."""

import time

from tino.config import Config
from tino.engine.game import Game
from tino.storage.highscore import JSONHighScoreStore
from tino.ui.input import InputHandler
from tino.ui.renderer import Renderer
from tino.ui.terminal import terminal_session

# Cap dt to avoid a physics/spawn spike on the very first frame or after
# a long stall (e.g. terminal resize taking time).
_MAX_DT = 0.1  # seconds


def run_app(config: Config | None = None) -> int:
    """Run the TINO terminal endless runner."""
    cfg = config or Config.load()
    high_score_store = JSONHighScoreStore()
    game = Game(config=cfg, high_score_store=high_score_store)

    frame_interval = 1.0 / max(10, cfg.target_fps)

    with terminal_session() as terminal:
        input_handler = InputHandler(terminal.stdscr, config=cfg)
        renderer = Renderer(terminal)

        last_time = time.perf_counter()

        while not game.should_quit:
            current_time = time.perf_counter()
            dt = min(current_time - last_time, _MAX_DT)
            last_time = current_time

            # Sync world width to current terminal width *before* ticking so
            # obstacle spawn positions are always correct for the visible area.
            _, term_width = terminal.dimensions
            game.world_width = float(term_width)

            # 1. Read input (non-blocking)
            action = input_handler.get_action()

            # 2. Process action & advance engine state
            game.handle_action(action)
            game.tick(dt)

            # 3. Render current frame
            renderer.render(game)

            # 4. Maintain fixed frame rate
            elapsed = time.perf_counter() - current_time
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    return 0
