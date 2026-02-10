"""Horizontal scrolling camera with parallax, scroll-lock zones, and 2-player midpoint tracking."""

from __future__ import annotations

from typing import Protocol

from blades_of_the_fallen_realm.settings import PLAYER_LEASH, SCREEN_WIDTH


class HasX(Protocol):
    """Structural type for any object with a mutable ``x`` attribute."""

    x: float


class Camera:
    """Horizontal scrolling camera for a side-scrolling beat 'em up.

    Features:
    - Tracks the midpoint of all active players' X positions.
    - Clamps to level bounds so the camera never shows outside the level.
    - Supports scroll-lock zones that freeze the camera until cleared.
    - Player leash blocks forward movement when a player exceeds
      ``PLAYER_LEASH`` pixels from the camera centre.
    - Parallax offset helper for multi-layer scrolling backgrounds.
    """

    def __init__(self) -> None:
        """Initialise the camera at position (0, 0) with no scroll lock."""
        self.x: float = 0.0
        self.y: float = 0.0
        self.scroll_locked: bool = False
        self.level_width: int = 0

    # --- scroll lock ---------------------------------------------------------

    def lock(self) -> None:
        """Engage scroll lock, preventing the camera from scrolling."""
        self.scroll_locked = True

    def unlock(self) -> None:
        """Release scroll lock, allowing the camera to resume tracking."""
        self.scroll_locked = False

    @property
    def is_locked(self) -> bool:
        """Return whether the camera is currently scroll-locked."""
        return self.scroll_locked

    # --- core update ---------------------------------------------------------

    def update(self, players: list[HasX], level_width: int) -> None:
        """Track the midpoint of all player X positions.

        The camera X is set to centre the midpoint on screen, then clamped
        to ``[0, level_width - SCREEN_WIDTH]`` so the view stays inside the
        level.  When scroll-locked the camera position is frozen.

        Args:
            players: List of player objects (must have an ``x`` attribute).
            level_width: Total width of the level in pixels.
        """
        self.level_width = level_width

        if self.scroll_locked:
            return

        if not players:
            return

        midpoint_x = sum(p.x for p in players) / len(players)
        self.x = midpoint_x - SCREEN_WIDTH / 2

        # Clamp to level bounds
        max_x = max(0, level_width - SCREEN_WIDTH)
        self.x = max(0.0, min(self.x, float(max_x)))

    # --- coordinate helpers --------------------------------------------------

    def apply(self, position: tuple[float, float]) -> tuple[float, float]:
        """Convert a world position to a screen position.

        Args:
            position: ``(world_x, world_y)`` coordinates.

        Returns:
            ``(screen_x, screen_y)`` after subtracting the camera offset.
        """
        return (position[0] - self.x, position[1] - self.y)

    def get_parallax_offset(self, layer_speed: float) -> float:
        """Return the horizontal scroll offset for a parallax layer.

        Args:
            layer_speed: Multiplier for scroll speed (e.g. 0.3 for far layer).

        Returns:
            The pixel offset to apply to the background layer.
        """
        return self.x * layer_speed

    # --- player leash --------------------------------------------------------

    def clamp_player(self, player: HasX) -> None:
        """Prevent a player from moving beyond the leash distance.

        If the player's X position is more than ``PLAYER_LEASH`` pixels from
        the camera centre, their X is clamped to the leash boundary.

        Args:
            player: A player object with a mutable ``x`` attribute.
        """
        camera_center_x = self.x + SCREEN_WIDTH / 2
        min_x = camera_center_x - PLAYER_LEASH
        max_x = camera_center_x + PLAYER_LEASH
        player.x = max(min_x, min(player.x, max_x))
