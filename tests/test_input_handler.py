"""Tests for InputHandler and PlayerControls classes."""

import pygame
import pytest

from blades_of_the_fallen_realm.engine.input_handler import (
    COMBO_WINDOW_MS,
    InputHandler,
    P1_CONTROLS,
    P2_CONTROLS,
    PlayerControls,
)


@pytest.fixture
def pygame_init() -> None:
    """Initialize pygame before each test."""
    pygame.init()
    pygame.display.set_mode((1, 1))  # Minimal display for testing


# ---------------------------------------------------------------------------
# PlayerControls tests
# ---------------------------------------------------------------------------


def test_p1_controls_arrow_keys(pygame_init: None) -> None:
    """P1 should use Arrow keys for directional input."""
    assert P1_CONTROLS.UP == pygame.K_UP
    assert P1_CONTROLS.DOWN == pygame.K_DOWN
    assert P1_CONTROLS.LEFT == pygame.K_LEFT
    assert P1_CONTROLS.RIGHT == pygame.K_RIGHT


def test_p1_controls_action_keys(pygame_init: None) -> None:
    """P1 should use Z/X/C for actions."""
    assert P1_CONTROLS.ATTACK == pygame.K_z
    assert P1_CONTROLS.JUMP == pygame.K_x
    assert P1_CONTROLS.MAGIC == pygame.K_c


def test_p2_controls_wasd_keys(pygame_init: None) -> None:
    """P2 should use WASD for directional input."""
    assert P2_CONTROLS.UP == pygame.K_w
    assert P2_CONTROLS.DOWN == pygame.K_s
    assert P2_CONTROLS.LEFT == pygame.K_a
    assert P2_CONTROLS.RIGHT == pygame.K_d


def test_p2_controls_action_keys(pygame_init: None) -> None:
    """P2 should use J/K/L for actions."""
    assert P2_CONTROLS.ATTACK == pygame.K_j
    assert P2_CONTROLS.JUMP == pygame.K_k
    assert P2_CONTROLS.MAGIC == pygame.K_l


def test_player_controls_dataclass() -> None:
    """PlayerControls should be a dataclass with correct fields."""
    custom_controls = PlayerControls(
        UP=pygame.K_i,
        DOWN=pygame.K_k,
        LEFT=pygame.K_j,
        RIGHT=pygame.K_l,
        ATTACK=pygame.K_a,
        JUMP=pygame.K_s,
        MAGIC=pygame.K_d,
    )
    assert custom_controls.UP == pygame.K_i
    assert custom_controls.ATTACK == pygame.K_a


# ---------------------------------------------------------------------------
# InputHandler initialization tests
# ---------------------------------------------------------------------------


def test_input_handler_initialization(pygame_init: None) -> None:
    """InputHandler should initialize with correct player_id and controls."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.player_id == 1
    assert handler.controls == P1_CONTROLS
    assert isinstance(handler.pressed, dict)
    assert isinstance(handler.just_pressed, dict)
    assert isinstance(handler.combo_buffer, list)


def test_input_handler_player_2_initialization(pygame_init: None) -> None:
    """InputHandler for player 2 should use P2_CONTROLS."""
    handler = InputHandler(2, P2_CONTROLS)
    assert handler.player_id == 2
    assert handler.controls == P2_CONTROLS


def test_input_handler_initial_state(pygame_init: None) -> None:
    """All actions should be False initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.pressed["UP"] is False
    assert handler.pressed["ATTACK"] is False
    assert handler.just_pressed["JUMP"] is False


# ---------------------------------------------------------------------------
# is_pressed tests
# ---------------------------------------------------------------------------


def test_is_pressed_returns_false_initially(pygame_init: None) -> None:
    """is_pressed should return False for all actions initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_pressed("UP") is False
    assert handler.is_pressed("ATTACK") is False
    assert handler.is_pressed("MAGIC") is False


def test_is_pressed_with_simulated_key(pygame_init: None) -> None:
    """is_pressed should return True when key state is manually set."""
    handler = InputHandler(1, P1_CONTROLS)
    # Simulate a key press
    handler.pressed["ATTACK"] = True
    assert handler.is_pressed("ATTACK") is True


def test_is_pressed_returns_false_for_unknown_action(pygame_init: None) -> None:
    """is_pressed should return False for unknown action strings."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_pressed("UNKNOWN") is False


# ---------------------------------------------------------------------------
# is_just_pressed tests
# ---------------------------------------------------------------------------


def test_is_just_pressed_returns_false_initially(pygame_init: None) -> None:
    """is_just_pressed should return False initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_just_pressed("ATTACK") is False
    assert handler.is_just_pressed("JUMP") is False


def test_is_just_pressed_with_simulated_press(pygame_init: None) -> None:
    """is_just_pressed should return True on the first frame of press."""
    handler = InputHandler(1, P1_CONTROLS)
    # Simulate just_pressed state
    handler.just_pressed["JUMP"] = True
    assert handler.is_just_pressed("JUMP") is True


def test_is_just_pressed_vs_held_state(pygame_init: None) -> None:
    """is_just_pressed should differ from is_pressed for held keys."""
    handler = InputHandler(1, P1_CONTROLS)
    # Simulate a held key
    handler.pressed["ATTACK"] = True
    handler.just_pressed["ATTACK"] = False
    assert handler.is_pressed("ATTACK") is True
    assert handler.is_just_pressed("ATTACK") is False


# ---------------------------------------------------------------------------
# get_direction tests
# ---------------------------------------------------------------------------


def test_get_direction_neutral(pygame_init: None) -> None:
    """get_direction should return (0, 0) when no direction is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.get_direction() == (0, 0)


def test_get_direction_up(pygame_init: None) -> None:
    """get_direction should return (0, -1) when UP is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    assert handler.get_direction() == (0, -1)


def test_get_direction_down(pygame_init: None) -> None:
    """get_direction should return (0, 1) when DOWN is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    assert handler.get_direction() == (0, 1)


def test_get_direction_left(pygame_init: None) -> None:
    """get_direction should return (-1, 0) when LEFT is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["LEFT"] = True
    assert handler.get_direction() == (-1, 0)


def test_get_direction_right(pygame_init: None) -> None:
    """get_direction should return (1, 0) when RIGHT is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["RIGHT"] = True
    assert handler.get_direction() == (1, 0)


def test_get_direction_up_left_diagonal(pygame_init: None) -> None:
    """get_direction should return (-1, -1) for diagonal up-left."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    handler.pressed["LEFT"] = True
    dx, dy = handler.get_direction()
    # Returns raw integer components without normalization
    assert dx == -1
    assert dy == -1


def test_get_direction_up_right_diagonal(pygame_init: None) -> None:
    """get_direction should return (1, -1) for diagonal up-right."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    handler.pressed["RIGHT"] = True
    dx, dy = handler.get_direction()
    assert dx == 1
    assert dy == -1


def test_get_direction_down_left_diagonal(pygame_init: None) -> None:
    """get_direction should return (-1, 1) for diagonal down-left."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    handler.pressed["LEFT"] = True
    dx, dy = handler.get_direction()
    assert dx == -1
    assert dy == 1


def test_get_direction_down_right_diagonal(pygame_init: None) -> None:
    """get_direction should return (1, 1) for diagonal down-right."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    handler.pressed["RIGHT"] = True
    dx, dy = handler.get_direction()
    assert dx == 1
    assert dy == 1


def test_get_direction_opposing_directions_cancel(pygame_init: None) -> None:
    """Pressing opposite directions should cancel out."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    handler.pressed["DOWN"] = True
    handler.pressed["LEFT"] = True
    handler.pressed["RIGHT"] = True
    assert handler.get_direction() == (0, 0)


# ---------------------------------------------------------------------------
# Combo buffer tests
# ---------------------------------------------------------------------------


def test_combo_buffer_starts_empty(pygame_init: None) -> None:
    """Combo buffer should be empty initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.get_combo_buffer() == []


def test_combo_buffer_stores_inputs(pygame_init: None) -> None:
    """Combo buffer should store inputs when actions are just pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    current_time = pygame.time.get_ticks()

    # Manually add to combo buffer
    handler.combo_buffer.append(("ATTACK", current_time))
    handler.combo_buffer.append(("ATTACK", current_time + 100))
    handler.combo_buffer.append(("JUMP", current_time + 200))

    buffer = handler.get_combo_buffer()
    assert len(buffer) == 3
    assert buffer == ["ATTACK", "ATTACK", "JUMP"]


def test_combo_buffer_expires_old_inputs(pygame_init: None) -> None:
    """Combo buffer should remove inputs older than COMBO_WINDOW_MS."""
    handler = InputHandler(1, P1_CONTROLS)
    old_time = pygame.time.get_ticks() - COMBO_WINDOW_MS - 100
    recent_time = pygame.time.get_ticks()

    # Add old and recent inputs
    handler.combo_buffer.append(("ATTACK", old_time))
    handler.combo_buffer.append(("JUMP", recent_time))

    # Call update to expire old inputs
    handler.update()

    buffer = handler.get_combo_buffer()
    # Old input should be removed
    assert "ATTACK" not in buffer or len([x for x in buffer if x == "ATTACK"]) == 0


def test_combo_buffer_keeps_last_3_inputs(pygame_init: None) -> None:
    """Combo buffer should keep only the last 3 inputs."""
    handler = InputHandler(1, P1_CONTROLS)
    current_time = pygame.time.get_ticks()

    # Add 5 inputs
    handler.combo_buffer.append(("ATTACK", current_time))
    handler.combo_buffer.append(("ATTACK", current_time + 10))
    handler.combo_buffer.append(("JUMP", current_time + 20))
    handler.combo_buffer.append(("MAGIC", current_time + 30))
    handler.combo_buffer.append(("ATTACK", current_time + 40))

    # Call update to trim buffer
    handler.update()

    buffer = handler.get_combo_buffer()
    # Should keep only last 3
    assert len(buffer) <= 3


def test_clear_buffer_empties_combo_buffer(pygame_init: None) -> None:
    """clear_buffer should empty the combo buffer."""
    handler = InputHandler(1, P1_CONTROLS)
    current_time = pygame.time.get_ticks()

    # Add some inputs
    handler.combo_buffer.append(("ATTACK", current_time))
    handler.combo_buffer.append(("JUMP", current_time + 100))

    assert len(handler.get_combo_buffer()) == 2

    # Clear buffer
    handler.clear_buffer()

    assert handler.get_combo_buffer() == []


# ---------------------------------------------------------------------------
# update() method tests
# ---------------------------------------------------------------------------


def test_update_method_exists(pygame_init: None) -> None:
    """update() should be callable without errors."""
    handler = InputHandler(1, P1_CONTROLS)
    # Should not raise
    handler.update()


def test_update_manages_combo_buffer(pygame_init: None) -> None:
    """update() should manage combo buffer expiration."""
    handler = InputHandler(1, P1_CONTROLS)
    old_time = pygame.time.get_ticks() - COMBO_WINDOW_MS - 200

    # Add an old input
    handler.combo_buffer.append(("ATTACK", old_time))

    # Call update
    handler.update()

    # Old input should be removed
    assert len(handler.get_combo_buffer()) == 0


# ---------------------------------------------------------------------------
# Gamepad detection tests (basic)
# ---------------------------------------------------------------------------


def test_gamepad_detection_no_crash(pygame_init: None) -> None:
    """Gamepad detection should not crash even if no gamepads are connected."""
    handler = InputHandler(1, P1_CONTROLS)
    # If no gamepads, joystick should be None
    # This test just verifies no crash occurs during initialization


def test_input_handler_has_joystick_attribute(pygame_init: None) -> None:
    """InputHandler should have a joystick attribute."""
    handler = InputHandler(1, P1_CONTROLS)
    assert hasattr(handler, "joystick")
    # Will be None if no gamepad is connected
