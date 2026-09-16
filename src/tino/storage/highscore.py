"""High score persistence interface and JSON implementation."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from tino.storage.paths import get_highscore_path


class HighScoreStore(Protocol):
    """Protocol defining the high score storage interface."""

    def load(self) -> int:
        """Load and return the current high score."""
        ...

    def save(self, score: int) -> None:
        """Save a new high score."""
        ...

    def reset(self) -> None:
        """Reset the stored high score back to 0."""
        ...


class JSONHighScoreStore:
    """JSON file-backed HighScoreStore implementation."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._path = file_path or get_highscore_path()

    @property
    def file_path(self) -> Path:
        return self._path

    def load(self) -> int:
        """Read high score from JSON file. Returns 0 if missing or invalid."""
        if not self._path.exists():
            return 0
        try:
            content = self._path.read_text(encoding="utf-8")
            data = json.loads(content)
            score = data.get("high_score", 0)
            return int(score) if isinstance(score, (int, float)) and score >= 0 else 0
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            return 0

    def save(self, score: int) -> None:
        """Save high score to JSON file."""
        score_val = max(0, int(score))
        data = {
            "high_score": score_val,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except OSError:
            # Silently degrade if file cannot be written
            pass

    def reset(self) -> None:
        """Reset stored high score to 0."""
        self.save(0)
