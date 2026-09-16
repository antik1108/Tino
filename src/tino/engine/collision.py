"""Pure collision detection functions."""

from tino.engine.entities import Rect


def check_collision(
    rect_a: Rect,
    rect_b: Rect,
    padding: float = 0.4,
) -> bool:
    """Determine whether two bounding rectangles overlap.

    Applies a small inner padding to prevent unfair edge grazing collisions.
    """
    # Shrink boxes slightly by padding for fair gameplay hitbox
    a_left = rect_a.x + padding
    a_right = rect_a.x + rect_a.width - padding
    a_bottom = rect_a.y + padding
    a_top = rect_a.y + rect_a.height - padding

    b_left = rect_b.x + padding
    b_right = rect_b.x + rect_b.width - padding
    b_bottom = rect_b.y + padding
    b_top = rect_b.y + rect_b.height - padding

    # Overlap check on 2D plane
    x_overlap = a_left < b_right and a_right > b_left
    y_overlap = a_bottom < b_top and a_top > b_bottom

    return x_overlap and y_overlap
