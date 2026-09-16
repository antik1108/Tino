"""Unit tests for HighScoreStore JSON persistence."""

import tempfile
import unittest
from pathlib import Path

from tino.storage.highscore import JSONHighScoreStore


class TestHighScoreStore(unittest.TestCase):
    """Test suite for high score JSON storage."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_zero(self):
        """Loading from a non-existent file returns 0 without failing."""
        non_existent = self.tmp_path / "does_not_exist.json"
        store = JSONHighScoreStore(file_path=non_existent)
        self.assertEqual(store.load(), 0)

    def test_corrupt_file_returns_zero(self):
        """Corrupted JSON file returns 0 gracefully."""
        corrupt_file = self.tmp_path / "corrupt.json"
        corrupt_file.write_text("{broken json 123", encoding="utf-8")

        store = JSONHighScoreStore(file_path=corrupt_file)
        self.assertEqual(store.load(), 0)

    def test_save_and_load_high_score(self):
        """Saved score is correctly read back from JSON file."""
        score_file = self.tmp_path / "highscore.json"
        store = JSONHighScoreStore(file_path=score_file)

        store.save(250)
        self.assertEqual(store.load(), 250)

        # Overwrite with higher score
        store.save(500)
        self.assertEqual(store.load(), 500)

    def test_reset_score(self):
        """Resetting score clears stored score back to 0."""
        score_file = self.tmp_path / "highscore.json"
        store = JSONHighScoreStore(file_path=score_file)

        store.save(420)
        self.assertEqual(store.load(), 420)

        store.reset()
        self.assertEqual(store.load(), 0)

    def test_invalid_negative_or_non_integer_handled(self):
        """Negative score or bad types are normalized."""
        score_file = self.tmp_path / "highscore.json"
        score_file.write_text('{"high_score": "not-a-number"}', encoding="utf-8")

        store = JSONHighScoreStore(file_path=score_file)
        self.assertEqual(store.load(), 0)


if __name__ == "__main__":
    unittest.main()
