"""Base entity class — position, HP, hitbox/hurtbox, state machine, velocity, invincibility."""

from __future__ import annotations

import pygame


class BaseEntity:
    """Base class for all game entities.

    Provides position (x, y for ground-plane, z for height), velocity,
    an image surface, and a ``draw`` method used by the renderer.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """Initialise a base entity at the given position.

        Args:
            x: Horizontal position in world space.
            y: Depth-axis position in world space (pseudo-3D Y).
        """
        self.x: float = x
        self.y: float = y
        self.z: float = 0.0
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.vel_z: float = 0.0
        self.image: pygame.Surface = pygame.Surface((0, 0), pygame.SRCALPHA)

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]) -> None:
        """Draw the entity to the screen, adjusted by camera offset.

        Args:
            screen: The target surface to blit onto.
            camera_offset: ``(offset_x, offset_y)`` camera translation.
        """
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - self.z - camera_offset[1]
        screen.blit(self.image, (draw_x, draw_y))
