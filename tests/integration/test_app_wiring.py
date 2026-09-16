"""Integration tests verifying app assembly and CLI interactions."""

import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tino.cli import cmd_score, create_parser, main
from tino.config import Config
from tino.engine.game import Game
from tino.storage.highscore import JSONHighScoreStore


class TestAppWiring(unittest.TestCase):
    """Integration test suite."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cli_parser_structure(self):
        """Verify CLI parser commands and flags."""
        parser = create_parser()

        # Help output check
        args_empty = parser.parse_args([])
        self.assertIsNone(args_empty.subcommand)

        args_score = parser.parse_args(["score"])
        self.assertEqual(args_score.subcommand, "score")

        args_reset = parser.parse_args(["reset-score", "--force"])
        self.assertEqual(args_reset.subcommand, "reset-score")
        self.assertTrue(args_reset.force)

    def test_cli_score_command(self):
        """'tino score' prints stored score to stdout."""
        score_file = self.tmp_path / "highscore.json"
        store = JSONHighScoreStore(file_path=score_file)
        store.save(750)

        with patch("tino.cli.JSONHighScoreStore", return_value=store):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                ret = cmd_score()
                self.assertEqual(ret, 0)
                self.assertIn("Current High Score: 750", mock_stdout.getvalue())

    def test_cli_reset_score_command(self):
        """'tino reset-score --force' resets score without prompt."""
        score_file = self.tmp_path / "highscore.json"
        store = JSONHighScoreStore(file_path=score_file)
        store.save(999)

        with patch("tino.cli.JSONHighScoreStore", return_value=store):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                ret = main(["reset-score", "--force"])
                self.assertEqual(ret, 0)
                self.assertEqual(store.load(), 0)
                self.assertIn("High score has been reset to 0.", mock_stdout.getvalue())

    def test_game_wiring_with_custom_store_and_config(self):
        """Game engine properly interfaces with Config and HighScoreStore."""
        config = Config(target_fps=60, initial_speed=30.0)
        store = JSONHighScoreStore(file_path=self.tmp_path / "highscore.json")
        store.save(120)

        game = Game(config=config, high_score_store=store, world_width=100.0)
        self.assertEqual(game.high_score, 120)
        self.assertEqual(game.config.target_fps, 60)
        self.assertEqual(game.world_width, 100.0)


if __name__ == "__main__":
    unittest.main()
