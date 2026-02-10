"""Tests for BaseEntity — draw, HP, state machine, gravity, invincibility."""

import pygame

from blades_of_the_fallen_realm.entities.base_entity import BaseEntity
from blades_of_the_fallen_realm.settings import GRAVITY, INVINCIBILITY_FRAMES

# ---------------------------------------------------------------------------
# Draw tests (existing)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# take_damage / HP tests
# ---------------------------------------------------------------------------


def test_take_damage_reduces_hp() -> None:
    """take_damage should reduce HP by the given amount."""
    entity = BaseEntity()
    entity.hp = 100
    entity.take_damage(30)
    assert entity.hp == 70


def test_take_damage_hp_does_not_go_negative() -> None:
    """HP should be clamped to 0, not go negative."""
    entity = BaseEntity()
    entity.hp = 10
    entity.take_damage(50)
    assert entity.hp == 0


def test_death_when_hp_reaches_zero() -> None:
    """Entity should be dead (is_alive False) when HP reaches 0."""
    entity = BaseEntity()
    entity.hp = 20
    entity.take_damage(20)
    assert entity.hp == 0
    assert entity.is_alive is False


def test_is_alive_true_when_hp_positive() -> None:
    """is_alive should be True when HP > 0."""
    entity = BaseEntity()
    assert entity.is_alive is True


# ---------------------------------------------------------------------------
# Invincibility tests
# ---------------------------------------------------------------------------


def test_invincibility_prevents_damage() -> None:
    """Damage should be ignored while invincibility_frames > 0."""
    entity = BaseEntity()
    entity.hp = 100
    entity.invincibility_frames = 10
    entity.take_damage(50)
    assert entity.hp == 100


def test_take_damage_grants_invincibility() -> None:
    """take_damage should grant INVINCIBILITY_FRAMES of invincibility."""
    entity = BaseEntity()
    entity.take_damage(10)
    assert entity.invincibility_frames == INVINCIBILITY_FRAMES


def test_invincibility_ticks_down_in_update() -> None:
    """update() should decrement invincibility_frames each call."""
    entity = BaseEntity()
    entity.invincibility_frames = 5
    entity.update(1.0 / 60.0)
    assert entity.invincibility_frames == 4


# ---------------------------------------------------------------------------
# State machine tests
# ---------------------------------------------------------------------------


def test_initial_state_is_idle() -> None:
    """Default state should be IDLE."""
    entity = BaseEntity()
    assert entity.state == "IDLE"


def test_change_state_transitions() -> None:
    """change_state should update the state string."""
    entity = BaseEntity()
    entity.change_state("WALK")
    assert entity.state == "WALK"
    entity.change_state("ATTACK")
    assert entity.state == "ATTACK"


def test_take_damage_sets_hit_state() -> None:
    """take_damage should transition state to HIT when entity survives."""
    entity = BaseEntity()
    entity.take_damage(10)
    assert entity.state == "HIT"


# ---------------------------------------------------------------------------
# Gravity / z-axis tests
# ---------------------------------------------------------------------------


def test_apply_gravity_increases_downward_velocity() -> None:
    """apply_gravity should decrease vel_z by GRAVITY."""
    entity = BaseEntity()
    entity.z = 50.0
    entity.vel_z = 0.0
    entity.apply_gravity()
    assert entity.vel_z == -GRAVITY


def test_entity_lands_at_z_zero() -> None:
    """Entity should land at z = 0 and vel_z should reset."""
    entity = BaseEntity()
    entity.z = 0.1
    entity.vel_z = -1.0
    entity.apply_gravity()
    assert entity.z == 0.0
    assert entity.vel_z == 0.0


def test_is_on_ground_true_when_z_zero() -> None:
    """is_on_ground should return True when z == 0."""
    entity = BaseEntity()
    entity.z = 0.0
    assert entity.is_on_ground() is True


def test_is_on_ground_true_when_z_negative() -> None:
    """is_on_ground should return True when z <= 0."""
    entity = BaseEntity()
    entity.z = -1.0
    assert entity.is_on_ground() is True


def test_is_on_ground_false_when_z_positive() -> None:
    """is_on_ground should return False when z > 0."""
    entity = BaseEntity()
    entity.z = 10.0
    assert entity.is_on_ground() is False


# ---------------------------------------------------------------------------
# Utility property / method tests
# ---------------------------------------------------------------------------


def test_get_position_returns_xy() -> None:
    """get_position should return (x, y) tuple."""
    entity = BaseEntity(x=10.0, y=20.0)
    assert entity.get_position() == (10.0, 20.0)


def test_velocity_property() -> None:
    """velocity property should return (vel_x, vel_y, vel_z) tuple."""
    entity = BaseEntity()
    entity.vel_x = 1.0
    entity.vel_y = 2.0
    entity.vel_z = 3.0
    assert entity.velocity == (1.0, 2.0, 3.0)


def test_default_facing_is_right() -> None:
    """Default facing should be 'right'."""
    entity = BaseEntity()
    assert entity.facing == "right"


def test_default_magic_charges() -> None:
    """Default magic charges should be 0."""
    entity = BaseEntity()
    assert entity.magic_charges == 0
