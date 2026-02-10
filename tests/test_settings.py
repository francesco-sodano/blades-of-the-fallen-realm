"""Tests for game constants defined in settings.py."""

from blades_of_the_fallen_realm.settings import (
    COOP_SPAWN_MULTIPLIER,
    FPS,
    MAX_MAGIC_CHARGES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


def test_screen_dimensions() -> None:
    """Verify screen dimensions are 960×540."""
    assert SCREEN_WIDTH == 960
    assert SCREEN_HEIGHT == 540


def test_fps() -> None:
    """Verify FPS is 60."""
    assert FPS == 60


def test_max_magic_charges() -> None:
    """Verify MAX_MAGIC_CHARGES is 9."""
    assert MAX_MAGIC_CHARGES == 9


def test_coop_spawn_multiplier() -> None:
    """Verify COOP_SPAWN_MULTIPLIER is 1.5."""
    assert COOP_SPAWN_MULTIPLIER == 1.5
