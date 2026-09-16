"""Unit tests for GameState transitions and Game engine state machine."""

import tempfile
import unittest
from pathlib import Path

from tino.engine.entities import Obstacle
from tino.engine.game import Game
from tino.engine.state import Action, GameState, is_valid_transition
from tino.storage.highscore import JSONHighScoreStore


class TestStateAndGame(unittest.TestCase):
    """Test suite for state machine and game ticks."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_state_transitions(self):
        """Verify legal state machine transitions."""
        self.assertTrue(is_valid_transition(GameState.MENU, GameState.PLAYING))
        self.assertTrue(is_valid_transition(GameState.PLAYING, GameState.GAME_OVER))
        self.assertTrue(is_valid_transition(GameState.GAME_OVER, GameState.PLAYING))
        self.assertTrue(is_valid_transition(GameState.GAME_OVER, GameState.MENU))

    def test_invalid_state_transitions(self):
        """Verify illegal transitions are rejected."""
        self.assertFalse(is_valid_transition(GameState.MENU, GameState.GAME_OVER))
        self.assertFalse(is_valid_transition(GameState.PLAYING, GameState.MENU))

    def test_game_menu_to_playing_action(self):
        """Sending START or JUMP action in MENU starts the game."""
        store = JSONHighScoreStore(file_path=self.tmp_path / "high_score.json")
        game = Game(high_score_store=store)
        self.assertEqual(game.state, GameState.MENU)

        game.handle_action(Action.START)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertEqual(game.score, 0)

    def test_game_score_advances_during_play(self):
        """Advancing ticks in PLAYING state increases elapsed time and score."""
        store = JSONHighScoreStore(file_path=self.tmp_path / "high_score.json")
        game = Game(high_score_store=store)
        game.start_game()

        # Tick 2.0 seconds
        game.tick(2.0)
        self.assertEqual(game.elapsed_time, 2.0)
        self.assertEqual(game.score, 20)

    def test_collision_triggers_game_over_and_saves_high_score(self):
        """Collision with obstacle transitions game to GAME_OVER and persists new record."""
        store = JSONHighScoreStore(file_path=self.tmp_path / "high_score.json")
        game = Game(high_score_store=store)
        game.start_game()

        # Advance time to earn score
        game.tick(5.0)  # score = 50
        self.assertEqual(game.score, 50)

        # Inject obstacle directly colliding with player at ground level
        game.obstacles.append(
            Obstacle(x=game.player.x, y=0.0, width=3.0, height=3.0)
        )

        # Tick to detect collision
        game.tick(0.01)
        self.assertEqual(game.state, GameState.GAME_OVER)
        self.assertTrue(game.is_new_high_score)
        self.assertEqual(game.high_score, 50)
        self.assertEqual(store.load(), 50)

    def test_game_restart_resets_entities(self):
        """Restarting after Game Over creates a fresh run with state PLAYING."""
        store = JSONHighScoreStore(file_path=self.tmp_path / "high_score.json")
        game = Game(high_score_store=store)
        game.start_game()
        game.state = GameState.GAME_OVER

        game.handle_action(Action.RESTART)
        self.assertEqual(game.state, GameState.PLAYING)
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.obstacles), 0)


if __name__ == "__main__":
    unittest.main()
