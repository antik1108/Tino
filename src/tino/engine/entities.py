"""Game entities: Player and Obstacles with movement arithmetic."""

from dataclasses import dataclass
from typing import NamedTuple


class Rect(NamedTuple):
    """Axis-Aligned Bounding Box."""

    x: float
    y: float
    width: float
    height: float


@dataclass
class Player:
    """Player entity (Dino) with single-jump physics."""

    x: float = 8.0
    y: float = 0.0  # 0.0 is ground level
    width: float = 5.0
    height: float = 4.0
    y_velocity: float = 0.0
    jump_strength: float = 18.0  # Initial jump velocity upwards
    gravity: float = 42.0  # Downward acceleration
    ground_y: float = 0.0

    @property
    def is_grounded(self) -> bool:
        """Check if player is resting on the ground."""
        return self.y <= self.ground_y and self.y_velocity == 0.0

    def jump(self) -> bool:
        """Initiate jump if on the ground. Returns True if jump was initiated."""
        if self.is_grounded:
            self.y_velocity = self.jump_strength
            return True
        return False

    def update(self, dt: float) -> None:
        """Advance player vertical physics by dt seconds."""
        if not self.is_grounded or self.y_velocity > 0:
            self.y += self.y_velocity * dt
            self.y_velocity -= self.gravity * dt

            # Land on ground
            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.y_velocity = 0.0

    @property
    def bounds(self) -> Rect:
        """Bounding rectangle for collision detection."""
        return Rect(self.x, self.y, self.width, self.height)


@dataclass
class Obstacle:
    """Ground obstacle entity moving towards the player."""

    x: float
    y: float = 0.0
    width: float = 3.0
    height: float = 3.0
    obstacle_type: str = "cactus"

    def update(self, dt: float, speed: float) -> None:
        """Move obstacle leftward based on world speed and dt."""
        self.x -= speed * dt

    @property
    def is_offscreen(self) -> bool:
        """Return True if obstacle has moved completely past the left edge."""
        return self.x + self.width < 0.0

    @property
    def bounds(self) -> Rect:
        """Bounding rectangle for collision detection."""
        return Rect(self.x, self.y, self.width, self.height)
