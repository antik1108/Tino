"""Difficulty curve: speed progression and obstacle spawn timings."""

import random


def calculate_speed(
    elapsed_time: float,
    initial_speed: float = 25.0,
    max_speed: float = 65.0,
    acceleration: float = 0.5,
) -> float:
    """Calculate current game speed based on elapsed survival time (seconds)."""
    return min(max_speed, initial_speed + (elapsed_time * acceleration))


def calculate_spawn_interval(
    current_speed: float,
    initial_speed: float = 25.0,
    base_min: float = 1.2,
    base_max: float = 2.8,
) -> float:
    """Calculate randomized time until next obstacle spawns.

    As speed increases, interval is compressed proportionally to maintain pacing.
    """
    speed_factor = max(1.0, current_speed / initial_speed)
    # Compress min and max intervals, but clamp to minimum safe clearance
    scaled_min = max(0.65, base_min / speed_factor)
    scaled_max = max(scaled_min + 0.3, base_max / speed_factor)

    return random.uniform(scaled_min, scaled_max)
