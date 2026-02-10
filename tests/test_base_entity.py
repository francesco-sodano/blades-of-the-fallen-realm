"""Tests for BaseEntity.draw() camera offset and z-height arithmetic."""

import pygame

from blades_of_the_fallen_realm.entities.base_entity import BaseEntity


def test_draw_zero_camera_offset() -> None:
    """draw() with zero offset should blit at (x, y - z)."""
    entity = BaseEntity(x=100.0, y=200.0)
    entity.z = 0.0
    entity.image = pygame.Surface((16, 16))
    entity.image.fill((255, 255, 255))

    screen = pygame.Surface((960, 540))
    screen.fill((0, 0, 0))
    entity.draw(screen, (0.0, 0.0))

    # Expected draw position: (100, 200)
    assert screen.get_at((100, 200)) == pygame.Color(255, 255, 255, 255)


def test_draw_nonzero_camera_offset() -> None:
    """draw() should subtract camera offset from position."""
    entity = BaseEntity(x=150.0, y=250.0)
    entity.z = 0.0
    entity.image = pygame.Surface((16, 16))
    entity.image.fill((255, 255, 255))

    screen = pygame.Surface((960, 540))
    screen.fill((0, 0, 0))
    entity.draw(screen, (50.0, 30.0))

    # Expected: (150 - 50, 250 - 0 - 30) = (100, 220)
    assert screen.get_at((100, 220)) == pygame.Color(255, 255, 255, 255)
    # Far away pixel should still be black
    assert screen.get_at((0, 0)) == pygame.Color(0, 0, 0, 255)


def test_draw_z_height_affects_position() -> None:
    """draw() should subtract z from the y draw coordinate (draw_y = y - z - offset_y)."""
    entity = BaseEntity(x=100.0, y=300.0)
    entity.z = 50.0
    entity.image = pygame.Surface((16, 16))
    entity.image.fill((255, 255, 255))

    screen = pygame.Surface((960, 540))
    screen.fill((0, 0, 0))
    entity.draw(screen, (0.0, 0.0))

    # Expected: (100, 300 - 50 - 0) = (100, 250)
    assert screen.get_at((100, 250)) == pygame.Color(255, 255, 255, 255)
    # The pixel at y=300 (without z offset) should be black
    assert screen.get_at((100, 300)) == pygame.Color(0, 0, 0, 255)


def test_draw_combined_z_and_camera_offset() -> None:
    """draw() with both z-height and camera offset should compute correctly."""
    entity = BaseEntity(x=200.0, y=300.0)
    entity.z = 40.0
    entity.image = pygame.Surface((16, 16))
    entity.image.fill((255, 255, 255))

    screen = pygame.Surface((960, 540))
    screen.fill((0, 0, 0))
    entity.draw(screen, (20.0, 10.0))

    # Expected: (200 - 20, 300 - 40 - 10) = (180, 250)
    assert screen.get_at((180, 250)) == pygame.Color(255, 255, 255, 255)
