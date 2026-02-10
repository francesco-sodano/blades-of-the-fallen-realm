"""Tests for the Y-sort depth-ordered Renderer."""

import pygame

from blades_of_the_fallen_realm.engine.renderer import Renderer
from blades_of_the_fallen_realm.entities.base_entity import BaseEntity
from blades_of_the_fallen_realm.settings import DEPTH_BAND_MAX, DEPTH_BAND_MIN

# --- add / remove entity ---


def test_add_entity() -> None:
    """Adding an entity should increase the render list."""
    renderer = Renderer()
    entity = BaseEntity(x=0.0, y=200.0)
    renderer.add_entity(entity)
    assert entity in renderer.entities


def test_remove_entity() -> None:
    """Removing an entity should decrease the render list."""
    renderer = Renderer()
    entity = BaseEntity(x=0.0, y=200.0)
    renderer.add_entity(entity)
    renderer.remove_entity(entity)
    assert entity not in renderer.entities


def test_add_multiple_entities() -> None:
    """Adding multiple entities should grow the render list."""
    renderer = Renderer()
    e1 = BaseEntity(x=0.0, y=200.0)
    e2 = BaseEntity(x=50.0, y=180.0)
    renderer.add_entity(e1)
    renderer.add_entity(e2)
    assert len(renderer.entities) == 2


# --- Y-sort ordering ---


def test_entities_sorted_by_y_position() -> None:
    """Entities should be sorted by Y position (ascending) during draw."""
    renderer = Renderer()
    high_y = BaseEntity(x=0.0, y=250.0)
    low_y = BaseEntity(x=0.0, y=170.0)
    renderer.add_entity(high_y)
    renderer.add_entity(low_y)

    draw_order: list[BaseEntity] = []
    original_draw = BaseEntity.draw

    def tracking_draw(
        self: BaseEntity,
        screen: pygame.Surface,
        camera_offset: tuple[float, float],
    ) -> None:
        draw_order.append(self)
        original_draw(self, screen, camera_offset)

    BaseEntity.draw = tracking_draw  # type: ignore[assignment]
    try:
        screen = pygame.Surface((960, 540))
        renderer.draw(screen, (0.0, 0.0))
    finally:
        BaseEntity.draw = original_draw  # type: ignore[assignment]

    assert draw_order[0] is low_y
    assert draw_order[1] is high_y


def test_lower_y_drawn_before_higher_y() -> None:
    """Entity at lower Y must be drawn before entity at higher Y."""
    renderer = Renderer()
    back = BaseEntity(x=10.0, y=160.0)
    front = BaseEntity(x=10.0, y=260.0)
    renderer.add_entity(front)
    renderer.add_entity(back)

    draw_order: list[BaseEntity] = []
    original_draw = BaseEntity.draw

    def tracking_draw(
        self: BaseEntity,
        screen: pygame.Surface,
        camera_offset: tuple[float, float],
    ) -> None:
        draw_order.append(self)
        original_draw(self, screen, camera_offset)

    BaseEntity.draw = tracking_draw  # type: ignore[assignment]
    try:
        screen = pygame.Surface((960, 540))
        renderer.draw(screen, (0.0, 0.0))
    finally:
        BaseEntity.draw = original_draw  # type: ignore[assignment]

    assert draw_order.index(back) < draw_order.index(front)


# --- Depth band clamping ---


def test_depth_band_clamp_below_min() -> None:
    """Entity Y below DEPTH_BAND_MIN should NOT be mutated by the renderer."""
    renderer = Renderer()
    original_y = float(DEPTH_BAND_MIN - 50)
    entity = BaseEntity(x=0.0, y=original_y)
    renderer.add_entity(entity)
    screen = pygame.Surface((960, 540))
    renderer.draw(screen, (0.0, 0.0))
    assert entity.y == original_y


def test_depth_band_clamp_above_max() -> None:
    """Entity Y above DEPTH_BAND_MAX should NOT be mutated by the renderer."""
    renderer = Renderer()
    original_y = float(DEPTH_BAND_MAX + 50)
    entity = BaseEntity(x=0.0, y=original_y)
    renderer.add_entity(entity)
    screen = pygame.Surface((960, 540))
    renderer.draw(screen, (0.0, 0.0))
    assert entity.y == original_y


def test_depth_band_within_bounds_unchanged() -> None:
    """Entity Y within bounds should not be changed."""
    renderer = Renderer()
    mid_y = float((DEPTH_BAND_MIN + DEPTH_BAND_MAX) / 2)
    entity = BaseEntity(x=0.0, y=mid_y)
    renderer.add_entity(entity)
    screen = pygame.Surface((960, 540))
    renderer.draw(screen, (0.0, 0.0))
    assert entity.y == mid_y


def test_draw_does_not_mutate_entity_y() -> None:
    """Renderer.draw() must never modify entity.y — clamping is sort-only."""
    renderer = Renderer()
    entity = BaseEntity(x=100.0, y=float(DEPTH_BAND_MAX + 100))
    renderer.add_entity(entity)
    screen = pygame.Surface((960, 540))
    renderer.draw(screen, (0.0, 0.0))
    assert entity.y == float(DEPTH_BAND_MAX + 100)


# --- Camera offset ---


def test_camera_offset_applied() -> None:
    """Camera offset should translate the entity draw position."""
    renderer = Renderer()
    entity = BaseEntity(x=100.0, y=200.0)
    entity.z = 0.0
    # Give the entity a 16×16 solid-white image.
    entity.image = pygame.Surface((16, 16))
    entity.image.fill((255, 255, 255))
    renderer.add_entity(entity)

    screen = pygame.Surface((960, 540))
    screen.fill((0, 0, 0))

    camera_offset = (30.0, 10.0)
    renderer.draw(screen, camera_offset)

    # Expected draw position: (100 - 30, 200 - 0 - 10) = (70, 190)
    expected_x = 70
    expected_y = 190
    # The pixel at the expected position should be white (drawn).
    assert screen.get_at((expected_x, expected_y)) == pygame.Color(255, 255, 255, 255)
    # A pixel far away from the draw area should still be black.
    assert screen.get_at((0, 0)) == pygame.Color(0, 0, 0, 255)
