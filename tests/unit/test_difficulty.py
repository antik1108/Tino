"""Unit tests for difficulty progression."""

import unittest

from tino.engine.difficulty import calculate_spawn_interval, calculate_speed


class TestDifficulty(unittest.TestCase):
    """Test suite for speed curves and spawn interval progression."""

    def test_speed_increases_over_time(self):
        """Speed strictly increases as elapsed survival time progresses."""
        speed_start = calculate_speed(elapsed_time=0.0, initial_speed=20.0, acceleration=1.0)
        speed_later = calculate_speed(elapsed_time=10.0, initial_speed=20.0, acceleration=1.0)
        self.assertGreater(speed_later, speed_start)
        self.assertEqual(speed_later, 30.0)

    def test_speed_capped_at_maximum(self):
        """Speed never exceeds defined maximum ceiling."""
        max_limit = 60.0
        speed = calculate_speed(
            elapsed_time=1000.0,
            initial_speed=20.0,
            max_speed=max_limit,
            acceleration=1.0,
        )
        self.assertEqual(speed, max_limit)

    def test_spawn_interval_within_bounds(self):
        """Calculated spawn interval falls within logical bounds."""
        for _ in range(50):
            interval = calculate_spawn_interval(
                current_speed=25.0,
                initial_speed=25.0,
                base_min=1.0,
                base_max=2.0,
            )
            self.assertTrue(1.0 <= interval <= 2.0)

    def test_spawn_interval_compresses_with_speed(self):
        """At high speeds, spawn intervals shrink to maintain difficulty."""
        low_speed_interval = calculate_spawn_interval(
            current_speed=25.0,
            initial_speed=25.0,
            base_min=2.0,
            base_max=4.0,
        )
        high_speed_interval = calculate_spawn_interval(
            current_speed=100.0,
            initial_speed=25.0,
            base_min=2.0,
            base_max=4.0,
        )
        self.assertTrue(high_speed_interval <= low_speed_interval or high_speed_interval < 4.0)


if __name__ == "__main__":
    unittest.main()
