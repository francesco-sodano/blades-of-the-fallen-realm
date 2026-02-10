"""Tests for the hitbox/hurtbox collision system."""

import pygame

from blades_of_the_fallen_realm.engine.collision import (
    HitboxData,
    check_hit,
    check_overlap,
    is_in_depth_range,
    resolve_ground_collision,
)
from blades_of_the_fallen_realm.settings import DEPTH_BAND_MAX, DEPTH_BAND_MIN

# --- check_overlap ---


def test_overlapping_rects_detect_collision() -> None:
    """Overlapping rectangles should be detected as colliding."""
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(25, 25, 50, 50)
    assert check_overlap(rect1, rect2) is True


def test_non_overlapping_rects_no_collision() -> None:
    """Non-overlapping rectangles should not be detected as colliding."""
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(100, 100, 50, 50)
    assert check_overlap(rect1, rect2) is False


def test_adjacent_rects_no_collision() -> None:
    """Rectangles sharing only an edge should not collide."""
    rect1 = pygame.Rect(0, 0, 50, 50)
    rect2 = pygame.Rect(50, 0, 50, 50)
    assert check_overlap(rect1, rect2) is False


# --- is_in_depth_range ---


def test_depth_within_tolerance() -> None:
    """Y positions within ±15px should pass the depth check."""
    assert is_in_depth_range(200.0, 210.0) is True


def test_depth_exactly_at_tolerance() -> None:
    """Y positions exactly at ±15px boundary should pass."""
    assert is_in_depth_range(200.0, 215.0) is True


def test_depth_outside_tolerance() -> None:
    """Y positions outside ±15px should fail the depth check."""
    assert is_in_depth_range(200.0, 216.0) is False


def test_depth_same_position() -> None:
    """Identical Y positions should always pass."""
    assert is_in_depth_range(200.0, 200.0) is True


def test_depth_custom_tolerance() -> None:
    """Custom tolerance should be respected."""
    assert is_in_depth_range(100.0, 130.0, tolerance=30.0) is True
    assert is_in_depth_range(100.0, 131.0, tolerance=30.0) is False


# --- check_hit ---


def test_check_hit_active_overlapping_in_range() -> None:
    """Hit should connect when hitbox active, rects overlap, and depth in range."""
    hitbox = HitboxData(rect=pygame.Rect(0, 0, 50, 50), active=True, damage=10)
    hurtbox = pygame.Rect(25, 25, 50, 50)
    assert check_hit(hitbox, hurtbox, 200.0, 210.0) is True


def test_check_hit_inactive_hitbox() -> None:
    """Hit should NOT connect when hitbox is inactive."""
    hitbox = HitboxData(rect=pygame.Rect(0, 0, 50, 50), active=False, damage=10)
    hurtbox = pygame.Rect(25, 25, 50, 50)
    assert check_hit(hitbox, hurtbox, 200.0, 200.0) is False


def test_check_hit_no_overlap() -> None:
    """Hit should NOT connect when rects don't overlap."""
    hitbox = HitboxData(rect=pygame.Rect(0, 0, 50, 50), active=True, damage=10)
    hurtbox = pygame.Rect(200, 200, 50, 50)
    assert check_hit(hitbox, hurtbox, 200.0, 200.0) is False


def test_check_hit_out_of_depth() -> None:
    """Hit should NOT connect when depth difference exceeds tolerance."""
    hitbox = HitboxData(rect=pygame.Rect(0, 0, 50, 50), active=True, damage=10)
    hurtbox = pygame.Rect(25, 25, 50, 50)
    assert check_hit(hitbox, hurtbox, 200.0, 250.0) is False


# --- resolve_ground_collision ---


def test_resolve_ground_collision_clamp_below_min() -> None:
    """Entity Y below depth_band_min should be clamped to min."""

    class _Entity:
        y: float = float(DEPTH_BAND_MIN - 50)

    entity = _Entity()
    resolve_ground_collision(entity, float(DEPTH_BAND_MIN), float(DEPTH_BAND_MAX))
    assert entity.y == DEPTH_BAND_MIN


def test_resolve_ground_collision_clamp_above_max() -> None:
    """Entity Y above depth_band_max should be clamped to max."""

    class _Entity:
        y: float = float(DEPTH_BAND_MAX + 50)

    entity = _Entity()
    resolve_ground_collision(entity, float(DEPTH_BAND_MIN), float(DEPTH_BAND_MAX))
    assert entity.y == DEPTH_BAND_MAX


def test_resolve_ground_collision_within_bounds() -> None:
    """Entity Y within bounds should remain unchanged."""
    mid_y = float((DEPTH_BAND_MIN + DEPTH_BAND_MAX) / 2)

    class _Entity:
        y: float = mid_y

    entity = _Entity()
    resolve_ground_collision(entity, float(DEPTH_BAND_MIN), float(DEPTH_BAND_MAX))
    assert entity.y == mid_y
