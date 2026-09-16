"""TINO Game Engine."""

from tino.engine.collision import check_collision
from tino.engine.difficulty import calculate_spawn_interval, calculate_speed
from tino.engine.entities import Obstacle, Player, Rect
from tino.engine.game import Game
from tino.engine.state import Action, GameState, is_valid_transition

__all__ = [
    "Action",
    "Game",
    "GameState",
    "Obstacle",
    "Player",
    "Rect",
    "calculate_spawn_interval",
    "calculate_speed",
    "check_collision",
    "is_valid_transition",
]
