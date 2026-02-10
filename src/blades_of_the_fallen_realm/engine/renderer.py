"""Y-sort depth-ordered renderer for pseudo-3D beat 'em up perspective."""

from __future__ import annotations

import pygame

from blades_of_the_fallen_realm.entities.base_entity import BaseEntity
from blades_of_the_fallen_realm.settings import DEPTH_BAND_MAX, DEPTH_BAND_MIN


class Renderer:
    """Renders entities with Y-sort depth ordering.

    Entities with a lower Y position (further from the camera) are drawn
    first so that entities closer to the viewer overlap those behind them.
    Entity Y positions are clamped for sorting purposes only; the actual
    ``y`` attribute is never modified by the renderer.
    """

    def __init__(self) -> None:
        """Initialise the renderer with an empty entity list."""
        self.entities: list[BaseEntity] = []

    def add_entity(self, entity: BaseEntity) -> None:
        """Register an entity for rendering.

        Args:
            entity: The entity to add to the render list.
        """
        self.entities.append(entity)

    def remove_entity(self, entity: BaseEntity) -> None:
        """Unregister an entity from rendering.

        Args:
            entity: The entity to remove from the render list.
        """
        self.entities.remove(entity)

    @staticmethod
    def _clamped_y(entity: BaseEntity) -> float:
        """Return the entity's Y clamped to the walkable depth band.

        This is used only for sorting/drawing and does **not** mutate
        the entity.

        Args:
            entity: The entity whose Y value to clamp.

        Returns:
            The clamped Y value.
        """
        return max(DEPTH_BAND_MIN, min(entity.y, DEPTH_BAND_MAX))

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]) -> None:
        """Sort entities by Y position and draw them in order.

        Entities are sorted using a clamped Y value within the depth band,
        but their actual ``y`` attribute is **not** modified.
        Lower Y values are drawn first (further back), higher Y values
        are drawn on top (closer to the camera).

        Args:
            screen: The target surface to draw onto.
            camera_offset: ``(offset_x, offset_y)`` camera translation.
        """
        sorted_entities = sorted(self.entities, key=self._clamped_y)

        for entity in sorted_entities:
            entity.draw(screen, camera_offset)
