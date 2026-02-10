"""Tests for InputHandler and PlayerControls classes."""

from typing import Any
from unittest.mock import MagicMock

import pygame

from blades_of_the_fallen_realm.engine.input_handler import (
    COMBO_WINDOW_MS,
    InputHandler,
    P1_CONTROLS,
    P2_CONTROLS,
    PlayerControls,
)

# ---------------------------------------------------------------------------
# PlayerControls tests
# ---------------------------------------------------------------------------


def test_p1_controls_arrow_keys() -> None:
    """P1 should use Arrow keys for directional input."""
    assert P1_CONTROLS.UP == pygame.K_UP
    assert P1_CONTROLS.DOWN == pygame.K_DOWN
    assert P1_CONTROLS.LEFT == pygame.K_LEFT
    assert P1_CONTROLS.RIGHT == pygame.K_RIGHT


def test_p1_controls_action_keys() -> None:
    """P1 should use Z/X/C for actions."""
    assert P1_CONTROLS.ATTACK == pygame.K_z
    assert P1_CONTROLS.JUMP == pygame.K_x
    assert P1_CONTROLS.MAGIC == pygame.K_c


def test_p2_controls_wasd_keys() -> None:
    """P2 should use WASD for directional input."""
    assert P2_CONTROLS.UP == pygame.K_w
    assert P2_CONTROLS.DOWN == pygame.K_s
    assert P2_CONTROLS.LEFT == pygame.K_a
    assert P2_CONTROLS.RIGHT == pygame.K_d


def test_p2_controls_action_keys() -> None:
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


def test_input_handler_initialization() -> None:
    """InputHandler should initialize with correct player_id and controls."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.player_id == 1
    assert handler.controls == P1_CONTROLS
    assert isinstance(handler.pressed, dict)
    assert isinstance(handler.just_pressed, dict)
    assert isinstance(handler.combo_buffer, list)


def test_input_handler_player_2_initialization() -> None:
    """InputHandler for player 2 should use P2_CONTROLS."""
    handler = InputHandler(2, P2_CONTROLS)
    assert handler.player_id == 2
    assert handler.controls == P2_CONTROLS


def test_input_handler_initial_state() -> None:
    """All actions should be False initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.pressed["UP"] is False
    assert handler.pressed["ATTACK"] is False
    assert handler.just_pressed["JUMP"] is False


# ---------------------------------------------------------------------------
# is_pressed tests
# ---------------------------------------------------------------------------


def test_is_pressed_returns_false_initially() -> None:
    """is_pressed should return False for all actions initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_pressed("UP") is False
    assert handler.is_pressed("ATTACK") is False
    assert handler.is_pressed("MAGIC") is False


def test_is_pressed_with_simulated_key() -> None:
    """is_pressed should return True when key state is manually set."""
    handler = InputHandler(1, P1_CONTROLS)
    # Simulate a key press
    handler.pressed["ATTACK"] = True
    assert handler.is_pressed("ATTACK") is True


def test_is_pressed_returns_false_for_unknown_action() -> None:
    """is_pressed should return False for unknown action strings."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_pressed("UNKNOWN") is False


# ---------------------------------------------------------------------------
# is_just_pressed tests
# ---------------------------------------------------------------------------


def test_is_just_pressed_returns_false_initially() -> None:
    """is_just_pressed should return False initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.is_just_pressed("ATTACK") is False
    assert handler.is_just_pressed("JUMP") is False


def test_is_just_pressed_with_simulated_press() -> None:
    """is_just_pressed should return True on the first frame of press."""
    handler = InputHandler(1, P1_CONTROLS)
    # Simulate just_pressed state
    handler.just_pressed["JUMP"] = True
    assert handler.is_just_pressed("JUMP") is True


def test_is_just_pressed_vs_held_state() -> None:
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


def test_get_direction_neutral() -> None:
    """get_direction should return (0, 0) when no direction is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.get_direction() == (0, 0)


def test_get_direction_up() -> None:
    """get_direction should return (0, -1) when UP is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    assert handler.get_direction() == (0, -1)


def test_get_direction_down() -> None:
    """get_direction should return (0, 1) when DOWN is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    assert handler.get_direction() == (0, 1)


def test_get_direction_left() -> None:
    """get_direction should return (-1, 0) when LEFT is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["LEFT"] = True
    assert handler.get_direction() == (-1, 0)


def test_get_direction_right() -> None:
    """get_direction should return (1, 0) when RIGHT is pressed."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["RIGHT"] = True
    assert handler.get_direction() == (1, 0)


def test_get_direction_up_left_diagonal() -> None:
    """get_direction should return (-1, -1) for diagonal up-left."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    handler.pressed["LEFT"] = True
    dx, dy = handler.get_direction()
    # Returns raw integer components without normalization
    assert dx == -1
    assert dy == -1


def test_get_direction_up_right_diagonal() -> None:
    """get_direction should return (1, -1) for diagonal up-right."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["UP"] = True
    handler.pressed["RIGHT"] = True
    dx, dy = handler.get_direction()
    assert dx == 1
    assert dy == -1


def test_get_direction_down_left_diagonal() -> None:
    """get_direction should return (-1, 1) for diagonal down-left."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    handler.pressed["LEFT"] = True
    dx, dy = handler.get_direction()
    assert dx == -1
    assert dy == 1


def test_get_direction_down_right_diagonal() -> None:
    """get_direction should return (1, 1) for diagonal down-right."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.pressed["DOWN"] = True
    handler.pressed["RIGHT"] = True
    dx, dy = handler.get_direction()
    assert dx == 1
    assert dy == 1


def test_get_direction_opposing_directions_cancel() -> None:
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


def test_combo_buffer_starts_empty() -> None:
    """Combo buffer should be empty initially."""
    handler = InputHandler(1, P1_CONTROLS)
    assert handler.get_combo_buffer() == []


def test_combo_buffer_stores_inputs() -> None:
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


def test_combo_buffer_expires_old_inputs() -> None:
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


def test_combo_buffer_keeps_last_3_inputs() -> None:
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


def test_clear_buffer_empties_combo_buffer() -> None:
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


def test_update_method_exists() -> None:
    """update() should be callable without errors."""
    handler = InputHandler(1, P1_CONTROLS)
    # Should not raise
    handler.update()


def test_update_manages_combo_buffer() -> None:
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


def test_gamepad_detection_no_crash() -> None:
    """Gamepad detection should not crash even if no gamepads are connected."""
    handler = InputHandler(1, P1_CONTROLS)
    # If no gamepads, joystick should be None
    # This test just verifies no crash occurs during initialization


def test_input_handler_has_joystick_attribute() -> None:
    """InputHandler should have a joystick attribute."""
    handler = InputHandler(1, P1_CONTROLS)
    assert hasattr(handler, "joystick")
    # Will be None if no gamepad is connected


# ---------------------------------------------------------------------------
# Gamepad mock tests — _check_gamepad_action()
# ---------------------------------------------------------------------------


def _make_mock_joystick(
    *,
    numhats: int = 0,
    numaxes: int = 0,
    numbuttons: int = 0,
    hat_value: tuple[int, int] = (0, 0),
    axis_values: dict[int, float] | None = None,
    button_values: dict[int, bool] | None = None,
) -> Any:
    """Create a mock joystick with configurable hat, axis, and button values."""
    joy = MagicMock()
    joy.get_numhats.return_value = numhats
    joy.get_numaxes.return_value = numaxes
    joy.get_numbuttons.return_value = numbuttons
    joy.get_hat.return_value = hat_value

    _axis = axis_values or {}
    joy.get_axis.side_effect = lambda i: _axis.get(i, 0.0)

    _btn = button_values or {}
    joy.get_button.side_effect = lambda i: _btn.get(i, False)

    return joy


def test_check_gamepad_action_returns_false_without_joystick() -> None:
    """_check_gamepad_action should return False when joystick is None."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = None
    assert handler._check_gamepad_action("UP") is False


def test_check_gamepad_up_hat() -> None:
    """D-pad hat up should register UP action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numhats=1, hat_value=(0, 1))
    assert handler._check_gamepad_action("UP") is True


def test_check_gamepad_up_axis() -> None:
    """Left stick up (axis 1 < -0.5) should register UP action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numaxes=2, axis_values={1: -0.8})
    assert handler._check_gamepad_action("UP") is True


def test_check_gamepad_down_hat() -> None:
    """D-pad hat down should register DOWN action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numhats=1, hat_value=(0, -1))
    assert handler._check_gamepad_action("DOWN") is True


def test_check_gamepad_down_axis() -> None:
    """Left stick down (axis 1 > 0.5) should register DOWN action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numaxes=2, axis_values={1: 0.8})
    assert handler._check_gamepad_action("DOWN") is True


def test_check_gamepad_left_hat() -> None:
    """D-pad hat left should register LEFT action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numhats=1, hat_value=(-1, 0))
    assert handler._check_gamepad_action("LEFT") is True


def test_check_gamepad_left_axis() -> None:
    """Left stick left (axis 0 < -0.5) should register LEFT action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numaxes=1, axis_values={0: -0.8})
    assert handler._check_gamepad_action("LEFT") is True


def test_check_gamepad_right_hat() -> None:
    """D-pad hat right should register RIGHT action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numhats=1, hat_value=(1, 0))
    assert handler._check_gamepad_action("RIGHT") is True


def test_check_gamepad_right_axis() -> None:
    """Left stick right (axis 0 > 0.5) should register RIGHT action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numaxes=1, axis_values={0: 0.8})
    assert handler._check_gamepad_action("RIGHT") is True


def test_check_gamepad_attack_button() -> None:
    """Button 0 should register ATTACK action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=1, button_values={0: True})
    assert handler._check_gamepad_action("ATTACK") is True


def test_check_gamepad_jump_button() -> None:
    """Button 1 should register JUMP action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=2, button_values={1: True})
    assert handler._check_gamepad_action("JUMP") is True


def test_check_gamepad_magic_button() -> None:
    """Button 2 should register MAGIC action."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=3, button_values={2: True})
    assert handler._check_gamepad_action("MAGIC") is True


def test_check_gamepad_unknown_action() -> None:
    """Unknown action should return False."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=3)
    assert handler._check_gamepad_action("UNKNOWN") is False


def test_check_gamepad_no_hats_no_axes() -> None:
    """Directional actions should return False when no hats or axes exist."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numhats=0, numaxes=0)
    assert handler._check_gamepad_action("UP") is False
    assert handler._check_gamepad_action("DOWN") is False
    assert handler._check_gamepad_action("LEFT") is False
    assert handler._check_gamepad_action("RIGHT") is False


def test_check_gamepad_no_buttons() -> None:
    """Button actions should return False when no buttons exist."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=0)
    assert handler._check_gamepad_action("ATTACK") is False
    assert handler._check_gamepad_action("JUMP") is False
    assert handler._check_gamepad_action("MAGIC") is False


def test_gamepad_or_keyboard_combined_update() -> None:
    """Gamepad input OR'd with keyboard state during update()."""
    handler = InputHandler(1, P1_CONTROLS)
    # Attach a mock gamepad that presses ATTACK
    handler.joystick = _make_mock_joystick(numbuttons=1, button_values={0: True})
    handler.update()
    # Even with no keyboard keys pressed, ATTACK should be True from gamepad
    assert handler.pressed["ATTACK"] is True


def test_gamepad_just_pressed_triggers_combo_buffer() -> None:
    """Gamepad just_pressed should add entries to the combo buffer."""
    handler = InputHandler(1, P1_CONTROLS)
    handler.joystick = _make_mock_joystick(numbuttons=1, button_values={0: True})
    # First update: ATTACK transitions from False → True → just_pressed
    handler.update()
    assert handler.just_pressed["ATTACK"] is True
    assert len(handler.combo_buffer) > 0
    assert handler.combo_buffer[-1][0] == "ATTACK"
