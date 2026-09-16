"""OS-appropriate storage path resolution."""

import os
import sys
from pathlib import Path


def get_data_dir() -> Path:
    """Resolve the per-user data directory for TINO.

    - macOS: ~/Library/Application Support/tino
    - Linux: $XDG_DATA_HOME/tino or ~/.local/share/tino
    - Other/Fallback: ~/.tino
    """
    home = Path.home()
    if sys.platform == "darwin":
        data_dir = home / "Library" / "Application Support" / "tino"
    elif sys.platform.startswith("linux"):
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            data_dir = Path(xdg_data) / "tino"
        else:
            data_dir = home / ".local" / "share" / "tino"
    else:
        data_dir = home / ".tino"

    return data_dir


def get_highscore_path() -> Path:
    """Return the path to the high score JSON file."""
    return get_data_dir() / "highscore.json"


def get_config_path() -> Path:
    """Return the path to the user config JSON file."""
    return get_data_dir() / "config.json"
