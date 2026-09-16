"""Storage package for TINO."""

from tino.storage.highscore import HighScoreStore, JSONHighScoreStore
from tino.storage.paths import get_config_path, get_data_dir, get_highscore_path

__all__ = [
    "HighScoreStore",
    "JSONHighScoreStore",
    "get_config_path",
    "get_data_dir",
    "get_highscore_path",
]
