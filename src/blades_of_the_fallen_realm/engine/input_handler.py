"""Input handler supporting 2 control schemes (P1/P2 keyboard) and gamepad auto-detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame

# Combo window constant (milliseconds)
COMBO_WINDOW_MS: int = 500


@dataclass
class PlayerControls:
    """Maps action strings to pygame key constants for a player.

    Attributes:
        UP: Key constant for moving up (into screen).
        DOWN: Key constant for moving down (toward camera).
        LEFT: Key constant for moving left.
        RIGHT: Key constant for moving right.
        ATTACK: Key constant for attack action.
        JUMP: Key constant for jump action.
        MAGIC: Key constant for magic action.
    """

    UP: int
    DOWN: int
    LEFT: int
    RIGHT: int
    ATTACK: int
    JUMP: int
    MAGIC: int


# Player 1 controls: Arrow keys + Z/X/C
P1_CONTROLS = PlayerControls(
    UP=pygame.K_UP,
    DOWN=pygame.K_DOWN,
    LEFT=pygame.K_LEFT,
    RIGHT=pygame.K_RIGHT,
    ATTACK=pygame.K_z,
    JUMP=pygame.K_x,
    MAGIC=pygame.K_c,
)

# Player 2 controls: WASD + J/K/L
P2_CONTROLS = PlayerControls(
    UP=pygame.K_w,
    DOWN=pygame.K_s,
    LEFT=pygame.K_a,
    RIGHT=pygame.K_d,
    ATTACK=pygame.K_j,
    JUMP=pygame.K_k,
    MAGIC=pygame.K_l,
)


class InputHandler:
    """Handles input for a single player, including keyboard and gamepad.

    Each player gets their own InputHandler instance with separate controls.
    Tracks pressed/just_pressed state and maintains a combo buffer for
    combo detection in beat 'em up gameplay.
    """

    def __init__(self, player_id: int, controls: PlayerControls) -> None:
        """Initialize the input handler for a player.

        Args:
            player_id: Player identifier (1 or 2).
            controls: PlayerControls instance mapping actions to keys.
        """
        self.player_id: int = player_id
        self.controls: PlayerControls = controls

        # Track current and previous frame state
        self.pressed: dict[str, bool] = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,
            "ATTACK": False,
            "JUMP": False,
            "MAGIC": False,
        }
        self.just_pressed: dict[str, bool] = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,
            "ATTACK": False,
            "JUMP": False,
            "MAGIC": False,
        }
        self._previous_pressed: dict[str, bool] = self.pressed.copy()

        # Combo buffer: stores (action, timestamp) tuples
        self.combo_buffer: list[tuple[str, int]] = []

        # Gamepad support
        self.joystick: Any = None  # pygame.joystick.Joystick | None
        self._detect_gamepad()

    def _detect_gamepad(self) -> None:
        """Auto-detect and assign a gamepad for this player.

        P1 gets joystick 0 (if available), P2 gets joystick 1 (if available).
        """
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        # Player 1 gets first gamepad, Player 2 gets second
        desired_index = self.player_id - 1

        if desired_index < joystick_count:
            self.joystick = pygame.joystick.Joystick(desired_index)
            self.joystick.init()

    def update(self) -> None:
        """Poll keyboard and gamepad state, update pressed/just_pressed dicts, and manage combo buffer.

        Call this once per frame before checking input state.
        """
        # Get current timestamp in milliseconds
        current_time = pygame.time.get_ticks()

        # Get keyboard state
        keys = pygame.key.get_pressed()

        # Map actions to their key states
        action_keys = {
            "UP": self.controls.UP,
            "DOWN": self.controls.DOWN,
            "LEFT": self.controls.LEFT,
            "RIGHT": self.controls.RIGHT,
            "ATTACK": self.controls.ATTACK,
            "JUMP": self.controls.JUMP,
            "MAGIC": self.controls.MAGIC,
        }

        # Update pressed state for each action
        for action, key_code in action_keys.items():
            current_state = keys[key_code]

            # Check for gamepad input as well
            if self.joystick:
                current_state = current_state or self._check_gamepad_action(action)

            self.pressed[action] = current_state

            # Determine if just pressed (pressed now but not in previous frame)
            self.just_pressed[action] = (
                current_state and not self._previous_pressed[action]
            )

            # Add to combo buffer if just pressed
            if self.just_pressed[action]:
                self.combo_buffer.append((action, current_time))

        # Update previous state for next frame
        self._previous_pressed = self.pressed.copy()

        # Remove expired inputs from combo buffer
        self.combo_buffer = [
            (action, timestamp)
            for action, timestamp in self.combo_buffer
            if current_time - timestamp <= COMBO_WINDOW_MS
        ]

        # Keep only last 3 inputs
        if len(self.combo_buffer) > 3:
            self.combo_buffer = self.combo_buffer[-3:]

    # Gamepad mapping: direction actions use hat + axis; button actions use button index.
    # Each direction entry: (hat_component, hat_threshold, axis_index, axis_threshold)
    #   hat_component: 0 = X-axis of hat, 1 = Y-axis of hat
    #   hat_threshold: value to compare against (> for positive, < for negative)
    #   axis_index: joystick axis index
    #   axis_threshold: threshold value (positive → >, negative → <)
    _DIRECTION_MAP: dict[str, tuple[int, int, int, float]] = {
        "UP": (1, 1, 1, -0.5),
        "DOWN": (1, -1, 1, 0.5),
        "LEFT": (0, -1, 0, -0.5),
        "RIGHT": (0, 1, 0, 0.5),
    }
    _BUTTON_MAP: dict[str, int] = {
        "ATTACK": 0,
        "JUMP": 1,
        "MAGIC": 2,
    }

    def _check_gamepad_action(self, action: str) -> bool:
        """Check if the given action is active on the gamepad.

        Args:
            action: Action string to check (UP, DOWN, LEFT, RIGHT, ATTACK, JUMP, MAGIC).

        Returns:
            True if the action is active on the gamepad.
        """
        if not self.joystick:
            return False

        if action in self._DIRECTION_MAP:
            hat_comp, hat_thresh, axis_idx, axis_thresh = self._DIRECTION_MAP[action]
            num_hats = self.joystick.get_numhats()
            num_axes = self.joystick.get_numaxes()

            hat = False
            if num_hats > 0:
                hat_val = self.joystick.get_hat(0)[hat_comp]
                if hat_thresh > 0:
                    hat = hat_val > 0
                else:
                    hat = hat_val < 0

            axis = False
            if num_axes > axis_idx:
                axis_val = self.joystick.get_axis(axis_idx)
                if axis_thresh > 0:
                    axis = axis_val > axis_thresh
                else:
                    axis = axis_val < axis_thresh

            return hat or axis

        if action in self._BUTTON_MAP:
            btn = self._BUTTON_MAP[action]
            if self.joystick.get_numbuttons() > btn:
                return bool(self.joystick.get_button(btn))
            return False

        return False

    def is_pressed(self, action: str) -> bool:
        """Check if an action key is currently held down.

        Args:
            action: Action string (UP, DOWN, LEFT, RIGHT, ATTACK, JUMP, MAGIC).

        Returns:
            True if the action key is currently pressed.
        """
        return self.pressed.get(action, False)

    def is_just_pressed(self, action: str) -> bool:
        """Check if an action key was pressed this frame (single frame detection).

        Args:
            action: Action string (UP, DOWN, LEFT, RIGHT, ATTACK, JUMP, MAGIC).

        Returns:
            True only on the first frame the key was pressed.
        """
        return self.just_pressed.get(action, False)

    def get_direction(self) -> tuple[int, int]:
        """Get the direction vector based on directional input.

        Returns:
            Tuple (dx, dy) where each component is -1, 0, or 1.
            Returns raw integer components without normalization,
            so diagonal movement will have magnitude √2.
        """
        dx = 0
        dy = 0

        if self.pressed["LEFT"]:
            dx -= 1
        if self.pressed["RIGHT"]:
            dx += 1
        if self.pressed["UP"]:
            dy -= 1
        if self.pressed["DOWN"]:
            dy += 1

        return (dx, dy)

    def get_combo_buffer(self) -> list[str]:
        """Get the list of recent actions within the combo window.

        Returns:
            List of action strings (most recent last) within COMBO_WINDOW_MS.
        """
        return [action for action, _ in self.combo_buffer]

    def clear_buffer(self) -> None:
        """Clear the combo buffer.

        Useful for resetting combos when a player is hit or performs a special move.
        """
        self.combo_buffer.clear()
