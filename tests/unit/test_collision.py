"""Unit tests for collision detection."""

import unittest

from tino.engine.collision import check_collision
from tino.engine.entities import Rect


class TestCollision(unittest.TestCase):
    """Test suite for bounding box collision checks."""

    def test_overlapping_rectangles(self):
        """Rectangles that clearly intersect must report collision."""
        rect_a = Rect(x=5.0, y=0.0, width=5.0, height=4.0)
        rect_b = Rect(x=7.0, y=0.0, width=3.0, height=3.0)
        self.assertTrue(check_collision(rect_a, rect_b))

    def test_separated_horizontally(self):
        """Rectangles with a horizontal gap must not collide."""
        rect_a = Rect(x=5.0, y=0.0, width=5.0, height=4.0)
        rect_b = Rect(x=15.0, y=0.0, width=3.0, height=3.0)
        self.assertFalse(check_collision(rect_a, rect_b))

    def test_separated_vertically(self):
        """Player jumping high above an obstacle must not collide."""
        rect_a = Rect(x=5.0, y=10.0, width=5.0, height=4.0)
        rect_b = Rect(x=6.0, y=0.0, width=3.0, height=3.0)
        self.assertFalse(check_collision(rect_a, rect_b))

    def test_identical_rectangles(self):
        """Identical overlapping rectangles must collide."""
        rect_a = Rect(x=10.0, y=0.0, width=4.0, height=4.0)
        rect_b = Rect(x=10.0, y=0.0, width=4.0, height=4.0)
        self.assertTrue(check_collision(rect_a, rect_b))


if __name__ == "__main__":
    unittest.main()
