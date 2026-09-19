"""Unit tests for Config loading and keybinding customizations."""

import json
import tempfile
import unittest
from pathlib import Path

from tino.config import Config


class TestConfig(unittest.TestCase):
    """Test suite for configuration loading and overrides."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_config_values(self):
        """Default configuration provides sane values."""
        config = Config()
        self.assertEqual(config.target_fps, 30)
        self.assertGreater(config.initial_speed, 0)
        jump = config.keybindings.jump
        self.assertTrue("space" in jump or " " in jump)
        quit_keys = config.keybindings.quit
        self.assertTrue("q" in quit_keys or "Q" in quit_keys)
        restart_keys = config.keybindings.restart
        self.assertTrue("r" in restart_keys or "R" in restart_keys)

    def test_load_non_existent_config_uses_defaults(self):
        """Missing config file loads default configuration without error."""
        path = self.tmp_path / "missing_config.json"
        config = Config.load(config_path=path)
        self.assertEqual(config.target_fps, 30)

    def test_load_valid_config_overrides_keybindings(self):
        """Custom keybindings in JSON override default mappings."""
        path = self.tmp_path / "custom_config.json"
        custom_data = {
            "target_fps": 60,
            "keybindings": {
                "jump": "j",
                "quit": "x",
                "restart": "p",
            },
        }
        path.write_text(json.dumps(custom_data), encoding="utf-8")

        config = Config.load(config_path=path)
        self.assertEqual(config.target_fps, 60)
        self.assertEqual(config.keybindings.jump, ("j",))
        self.assertEqual(config.keybindings.quit, ("x",))
        self.assertEqual(config.keybindings.restart, ("p",))

    def test_load_ignores_unknown_keys(self):
        """Unknown JSON keys are ignored gracefully without error."""
        path = self.tmp_path / "future_config.json"
        custom_data = {
            "unknown_setting": "foobar",
            "theme": "dark_matrix",
            "schema_version": 2,
        }
        path.write_text(json.dumps(custom_data), encoding="utf-8")

        config = Config.load(config_path=path)
        self.assertEqual(config.target_fps, 30)

    def test_load_corrupt_config_falls_back(self):
        """Corrupt JSON falls back to default config without crash."""
        path = self.tmp_path / "corrupt_config.json"
        path.write_text("{not: valid: json", encoding="utf-8")

        config = Config.load(config_path=path)
        self.assertEqual(config.target_fps, 30)


if __name__ == "__main__":
    unittest.main()
