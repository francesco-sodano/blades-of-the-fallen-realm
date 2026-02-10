"""Tests for the horizontal scrolling Camera."""

from blades_of_the_fallen_realm.engine.camera import Camera
from blades_of_the_fallen_realm.settings import (
    PARALLAX_FAR,
    PARALLAX_MID,
    PARALLAX_NEAR,
    PLAYER_LEASH,
    SCREEN_WIDTH,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _MockPlayer:
    """Minimal stand-in for a player entity with an ``x`` attribute."""

    def __init__(self, x: float = 0.0) -> None:
        self.x = x


# ---------------------------------------------------------------------------
# Midpoint tracking — 1 player
# ---------------------------------------------------------------------------


def test_track_single_player(camera: Camera) -> None:
    """Camera should centre on a single player's X position."""
    player = _MockPlayer(x=600.0)
    camera.update([player], 3000)
    expected_x = 600.0 - SCREEN_WIDTH / 2
    assert camera.x == expected_x


def test_track_single_player_at_origin(camera: Camera) -> None:
    """Camera should clamp to 0 when a single player is at the origin."""
    player = _MockPlayer(x=0.0)
    camera.update([player], 3000)
    assert camera.x == 0.0


# ---------------------------------------------------------------------------
# Midpoint tracking — 2 players
# ---------------------------------------------------------------------------


def test_track_two_players(camera: Camera) -> None:
    """Camera should centre on the midpoint of two players."""
    p1 = _MockPlayer(x=400.0)
    p2 = _MockPlayer(x=800.0)
    camera.update([p1, p2], 3000)
    midpoint = (400.0 + 800.0) / 2  # 600
    expected_x = midpoint - SCREEN_WIDTH / 2
    assert camera.x == expected_x


def test_track_two_players_midpoint_values(camera: Camera) -> None:
    """Verify exact midpoint arithmetic with two asymmetric positions."""
    p1 = _MockPlayer(x=100.0)
    p2 = _MockPlayer(x=500.0)
    camera.update([p1, p2], 3000)
    midpoint = (100.0 + 500.0) / 2  # 300
    expected_x = midpoint - SCREEN_WIDTH / 2
    # Clamp to 0 since expected_x would be negative
    assert camera.x == max(0.0, expected_x)


# ---------------------------------------------------------------------------
# Scroll lock
# ---------------------------------------------------------------------------


def test_scroll_lock_stops_camera(camera: Camera) -> None:
    """When scroll-locked the camera position must not change."""
    player = _MockPlayer(x=1000.0)
    camera.update([player], 3000)
    original_x = camera.x

    camera.lock()
    assert camera.is_locked is True

    # Move player further — camera should stay put
    player.x = 2000.0
    camera.update([player], 3000)
    assert camera.x == original_x


def test_scroll_unlock_resumes_tracking(camera: Camera) -> None:
    """After unlocking, camera should resume tracking the player."""
    player = _MockPlayer(x=1000.0)
    camera.update([player], 3000)

    camera.lock()
    player.x = 2000.0
    camera.update([player], 3000)

    camera.unlock()
    assert camera.is_locked is False

    camera.update([player], 3000)
    expected_x = 2000.0 - SCREEN_WIDTH / 2
    assert camera.x == expected_x


# ---------------------------------------------------------------------------
# Parallax offsets
# ---------------------------------------------------------------------------


def test_parallax_far_offset(camera: Camera) -> None:
    """FAR layer offset should be camera.x * PARALLAX_FAR."""
    camera.x = 500.0
    assert camera.get_parallax_offset(PARALLAX_FAR) == 500.0 * PARALLAX_FAR


def test_parallax_mid_offset(camera: Camera) -> None:
    """MID layer offset should be camera.x * PARALLAX_MID."""
    camera.x = 500.0
    assert camera.get_parallax_offset(PARALLAX_MID) == 500.0 * PARALLAX_MID


def test_parallax_near_offset(camera: Camera) -> None:
    """NEAR layer offset should equal camera.x (1.0x multiplier)."""
    camera.x = 500.0
    assert camera.get_parallax_offset(PARALLAX_NEAR) == 500.0


# ---------------------------------------------------------------------------
# Level bounds clamping
# ---------------------------------------------------------------------------


def test_clamp_to_left_bound(camera: Camera) -> None:
    """Camera X must never go below 0."""
    player = _MockPlayer(x=0.0)
    camera.update([player], 3000)
    assert camera.x >= 0.0


def test_clamp_to_right_bound(camera: Camera) -> None:
    """Camera X must never exceed level_width - SCREEN_WIDTH."""
    level_width = 2000
    player = _MockPlayer(x=float(level_width))
    camera.update([player], level_width)
    assert camera.x <= level_width - SCREEN_WIDTH


def test_clamp_level_smaller_than_screen(camera: Camera) -> None:
    """When the level is smaller than the screen the camera stays at 0."""
    player = _MockPlayer(x=100.0)
    camera.update([player], SCREEN_WIDTH // 2)
    assert camera.x == 0.0


# ---------------------------------------------------------------------------
# Player leash
# ---------------------------------------------------------------------------


def test_player_leash_blocks_forward_movement(camera: Camera) -> None:
    """Player should be clamped if beyond PLAYER_LEASH from camera centre."""
    camera.x = 0.0
    camera_center = SCREEN_WIDTH / 2
    player = _MockPlayer(x=camera_center + PLAYER_LEASH + 100)
    camera.clamp_player(player)
    assert player.x == camera_center + PLAYER_LEASH


def test_player_leash_blocks_backward_movement(camera: Camera) -> None:
    """Player should be clamped if behind camera centre by more than leash."""
    camera.x = 500.0
    camera_center = 500.0 + SCREEN_WIDTH / 2
    player = _MockPlayer(x=camera_center - PLAYER_LEASH - 50)
    camera.clamp_player(player)
    assert player.x == camera_center - PLAYER_LEASH


def test_player_within_leash_unchanged(camera: Camera) -> None:
    """Player inside the leash boundary should not be moved."""
    camera.x = 0.0
    camera_center = SCREEN_WIDTH / 2
    original_x = camera_center + 100
    player = _MockPlayer(x=original_x)
    camera.clamp_player(player)
    assert player.x == original_x


# ---------------------------------------------------------------------------
# apply() — world to screen
# ---------------------------------------------------------------------------


def test_apply_converts_world_to_screen(camera: Camera) -> None:
    """apply() should subtract camera position from world coordinates."""
    camera.x = 100.0
    camera.y = 50.0
    sx, sy = camera.apply((300.0, 200.0))
    assert sx == 200.0
    assert sy == 150.0


def test_apply_zero_offset(camera: Camera) -> None:
    """When camera is at origin, apply() returns the same position."""
    sx, sy = camera.apply((42.0, 99.0))
    assert sx == 42.0
    assert sy == 99.0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_update_with_no_players(camera: Camera) -> None:
    """Updating with an empty player list should not change the camera."""
    camera.x = 123.0
    camera.update([], 3000)
    assert camera.x == 123.0


def test_is_locked_property_default(camera: Camera) -> None:
    """Camera should not be locked by default."""
    assert camera.is_locked is False
