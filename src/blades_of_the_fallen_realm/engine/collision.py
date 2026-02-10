"""Hitbox/hurtbox collision system with depth proximity checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pygame

from blades_of_the_fallen_realm.settings import DEPTH_PROXIMITY


class HasY(Protocol):
    """Structural type for any object with a mutable ``y`` attribute."""

    y: float


@dataclass
class HitboxData:
    """Collision data for an attack hitbox.

    Attributes:
        rect: The collision rectangle.
        active: Whether the hitbox is currently active (only during attack frames).
        damage: Damage dealt on hit.
    """

    rect: pygame.Rect
    active: bool
    damage: int


def check_overlap(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check whether two rectangles overlap.

    Args:
        rect1: First rectangle.
        rect2: Second rectangle.

    Returns:
        True if the rectangles overlap, False otherwise.
    """
    return rect1.colliderect(rect2)


def is_in_depth_range(y1: float, y2: float, tolerance: float = DEPTH_PROXIMITY) -> bool:
    """Check whether two Y-depth values are within tolerance of each other.

    Args:
        y1: First Y-depth position.
        y2: Second Y-depth position.
        tolerance: Maximum allowed difference (default ``DEPTH_PROXIMITY``).

    Returns:
        True if ``abs(y1 - y2) <= tolerance``.
    """
    return abs(y1 - y2) <= tolerance


def check_hit(
    attacker_hitbox: HitboxData,
    defender_hurtbox: pygame.Rect,
    attacker_y: float,
    defender_y: float,
) -> bool:
    """Determine whether an attack connects with a defender.

    An attack connects when all three conditions are met:
    1. The attacker's hitbox is active.
    2. The hitbox rectangle overlaps the defender's hurtbox rectangle.
    3. The attacker and defender are within ``DEPTH_PROXIMITY`` on the Y-axis.

    Args:
        attacker_hitbox: The attacker's hitbox data.
        defender_hurtbox: The defender's hurtbox rectangle.
        attacker_y: The attacker's Y-depth position.
        defender_y: The defender's Y-depth position.

    Returns:
        True if the hit connects, False otherwise.
    """
    if not attacker_hitbox.active:
        return False
    if not check_overlap(attacker_hitbox.rect, defender_hurtbox):
        return False
    return is_in_depth_range(attacker_y, defender_y)


def resolve_ground_collision(
    entity: HasY,
    depth_band_min: float,
    depth_band_max: float,
) -> None:
    """Clamp an entity's Y position within the walkable depth band.

    Args:
        entity: Any object with a ``y`` attribute (e.g. :class:`BaseEntity`).
        depth_band_min: Top of the walkable depth band (minimum Y).
        depth_band_max: Bottom of the walkable depth band (maximum Y).
    """
    if entity.y < depth_band_min:
        entity.y = depth_band_min
    elif entity.y > depth_band_max:
        entity.y = depth_band_max
