"""Configuration loader and settings defaults."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from tino.storage.paths import get_config_path


@dataclass(frozen=True)
class KeyBindings:
    """Key bindings mapping."""

    jump: tuple[str, ...] = (" ", "space", "KEY_UP", "w")
    quit: tuple[str, ...] = ("q", "Q", "\x03")  # 'q' or Ctrl+C
    restart: tuple[str, ...] = ("r", "R")


@dataclass
class Config:
    """Game configuration."""

    target_fps: int = 30
    initial_speed: float = 25.0
    max_speed: float = 65.0
    speed_acceleration: float = 0.5  # speed increase per second
    base_spawn_min_interval: float = 1.2  # seconds between obstacles
    base_spawn_max_interval: float = 2.8
    keybindings: KeyBindings = field(default_factory=KeyBindings)

    @classmethod
    def load(cls, config_path: Path | None = None) -> "Config":
        """Load configuration from optional JSON file, merging over defaults."""
        path = config_path or get_config_path()
        config = cls()

        if not path.exists():
            return config

        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
            if not isinstance(data, dict):
                return config

            # Parse custom keybindings if present
            kb_data = data.get("keybindings")
            if isinstance(kb_data, dict):
                jump_bind = kb_data.get("jump")
                quit_bind = kb_data.get("quit")
                restart_bind = kb_data.get("restart")

                jump_list = list(config.keybindings.jump)
                if isinstance(jump_bind, str) and jump_bind:
                    jump_list = [jump_bind]
                elif isinstance(jump_bind, list):
                    jump_list = [str(k) for k in jump_bind]

                quit_list = list(config.keybindings.quit)
                if isinstance(quit_bind, str) and quit_bind:
                    quit_list = [quit_bind]
                elif isinstance(quit_bind, list):
                    quit_list = [str(k) for k in quit_bind]

                restart_list = list(config.keybindings.restart)
                if isinstance(restart_bind, str) and restart_bind:
                    restart_list = [restart_bind]
                elif isinstance(restart_bind, list):
                    restart_list = [str(k) for k in restart_bind]

                config.keybindings = KeyBindings(
                    jump=tuple(jump_list),
                    quit=tuple(quit_list),
                    restart=tuple(restart_list),
                )

            # Numerical overrides if provided
            if "target_fps" in data and isinstance(data["target_fps"], int) and data["target_fps"] > 0:
                config.target_fps = data["target_fps"]

        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            # Gracefully ignore invalid config file
            pass

        return config
