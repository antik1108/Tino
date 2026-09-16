"""Unit tests for Player and Obstacle entity mechanics."""

import unittest

from tino.engine.entities import Obstacle, Player


class TestEntities(unittest.TestCase):
    """Test suite for player physics and obstacle movement."""

    def test_player_initial_state(self):
        """Player starts on ground with zero vertical velocity."""
        player = Player()
        self.assertEqual(player.y, 0.0)
        self.assertTrue(player.is_grounded)
        self.assertEqual(player.y_velocity, 0.0)

    def test_player_jump_initiates_velocity(self):
        """Jumping from ground sets positive vertical velocity."""
        player = Player()
        jump_success = player.jump()
        self.assertTrue(jump_success)
        self.assertGreater(player.y_velocity, 0.0)

    def test_player_prevents_double_jump(self):
        """Player cannot jump again while mid-air."""
        player = Player()
        player.jump()
        # Advance time slightly so player is airborne
        player.update(0.1)
        self.assertGreater(player.y, 0.0)
        self.assertFalse(player.is_grounded)

        # Second jump attempt should fail
        second_jump = player.jump()
        self.assertFalse(second_jump)

    def test_player_gravity_and_landing(self):
        """Player jumps, ascends, descends via gravity, and lands safely at ground."""
        player = Player()
        player.jump()

        # Ascending
        player.update(0.1)
        mid_air_y = player.y
        self.assertGreater(mid_air_y, 0.0)

        # Advance enough time to complete jump arc and land (1.5 seconds)
        for _ in range(15):
            player.update(0.1)

        self.assertEqual(player.y, player.ground_y)
        self.assertEqual(player.y_velocity, 0.0)
        self.assertTrue(player.is_grounded)

    def test_obstacle_movement(self):
        """Obstacle moves leftward according to speed and dt."""
        obstacle = Obstacle(x=100.0, width=3.0, height=3.0)
        speed = 20.0
        dt = 0.5  # 20 * 0.5 = 10 units leftward
        obstacle.update(dt, speed)
        self.assertEqual(obstacle.x, 90.0)
        self.assertFalse(obstacle.is_offscreen)

    def test_obstacle_offscreen_detection(self):
        """Obstacle is offscreen only when completely past left edge."""
        obstacle = Obstacle(x=1.0, width=3.0, height=3.0)
        self.assertFalse(obstacle.is_offscreen)

        obstacle.x = -2.0  # part still in view (since width is 3.0, right edge is +1.0)
        self.assertFalse(obstacle.is_offscreen)

        obstacle.x = -4.0  # completely offscreen
        self.assertTrue(obstacle.is_offscreen)


if __name__ == "__main__":
    unittest.main()
