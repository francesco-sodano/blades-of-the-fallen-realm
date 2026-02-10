"""Base entity class — foundation for all game entities.

Provides position, HP, state machine, hitbox/hurtbox, gravity,
invincibility frames, and core update/draw methods.
"""

from __future__ import annotations

import pygame

from blades_of_the_fallen_realm.engine.collision import HitboxData
from blades_of_the_fallen_realm.settings import GRAVITY, INVINCIBILITY_FRAMES


class BaseEntity:
    """Base class for all game entities.

    All game entities (players, enemies, bosses, mounts, pickups) inherit
    from this class.  It provides position (x, y for ground-plane, z for
    height), HP, a string-based state machine, hitbox/hurtbox rectangles,
    gravity, invincibility frames, and core update/draw methods.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """Initialise a base entity at the given position.

        Args:
            x: Horizontal position in world space.
            y: Depth-axis position in world space (pseudo-3D Y).
        """
        # Position
        self.x: float = x
        self.y: float = y
        self.z: float = 0.0

        # Velocity
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.vel_z: float = 0.0

        # Health
        self.hp: int = 100
        self.max_hp: int = 100

        # Magic
        self.magic_charges: int = 0

        # State machine (string enums, not integers)
        self.state: str = "IDLE"
        self.facing: str = "right"

        # Collision
        self.hitbox: HitboxData = HitboxData(
            rect=pygame.Rect(0, 0, 0, 0), active=False, damage=0
        )
        self.hurtbox: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        # Invincibility
        self.invincibility_frames: int = 0

        # Visual
        self.image: pygame.Surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.sprite: pygame.Surface | None = None

    @property
    def is_alive(self) -> bool:
        """Return whether the entity is still alive.

        Returns:
            True if ``hp > 0``, False otherwise.
        """
        return self.hp > 0

    @property
    def velocity(self) -> tuple[float, float, float]:
        """Return the velocity as a tuple.

        Returns:
            ``(vel_x, vel_y, vel_z)`` velocity components.
        """
        return (self.vel_x, self.vel_y, self.vel_z)

    def get_position(self) -> tuple[float, float]:
        """Return the ground-plane position.

        Returns:
            ``(x, y)`` position on the ground plane.
        """
        return (self.x, self.y)

    def is_on_ground(self) -> bool:
        """Check whether the entity is on the ground.

        Returns:
            True if ``z <= 0``, False otherwise.
        """
        return self.z <= 0.0

    def change_state(self, new_state: str) -> None:
        """Transition the entity's state machine to a new state.

        Args:
            new_state: The target state string (e.g. ``"IDLE"``, ``"HIT"``).
        """
        self.state = new_state

    def take_damage(self, amount: int) -> None:
        """Reduce HP by *amount* and grant invincibility frames.

        Damage is ignored while ``invincibility_frames > 0``.  When HP
        reaches zero the entity is considered dead (``is_alive`` returns
        ``False``).

        Args:
            amount: The amount of damage to inflict.
        """
        if self.invincibility_frames > 0:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp > 0:
            self.change_state("HIT")
        self.invincibility_frames = INVINCIBILITY_FRAMES

    def apply_gravity(self) -> None:
        """Apply gravity to the vertical velocity and land at z = 0.

        Gravity is applied per frame (fixed-timestep at 60 FPS) matching
        the retro arcade physics model.  ``GRAVITY`` is subtracted from
        ``vel_z`` each call.  If the entity falls to or below ground
        level, ``z`` is clamped to 0 and ``vel_z`` is reset.
        """
        self.vel_z -= GRAVITY
        self.z += self.vel_z
        if self.z <= 0.0:
            self.z = 0.0
            self.vel_z = 0.0

    def update(self, dt: float) -> None:
        """Update entity state each frame.

        Applies velocity to position, ticks invincibility frames, and
        applies gravity when airborne.  Gravity and invincibility are
        frame-count based (fixed 60 FPS timestep) consistent with the
        retro arcade physics model used by ``GRAVITY`` and
        ``INVINCIBILITY_FRAMES`` constants.

        Args:
            dt: Delta time since last frame (seconds).
        """
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        if not self.is_on_ground():
            self.apply_gravity()

        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1

    def draw(self, screen: pygame.Surface, camera_offset: tuple[float, float]) -> None:
        """Draw the entity to the screen, adjusted by camera offset.

        If a ``sprite`` is set it is used; otherwise the ``image``
        surface is drawn.

        Args:
            screen: The target surface to blit onto.
            camera_offset: ``(offset_x, offset_y)`` camera translation.
        """
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - self.z - camera_offset[1]
        surface = self.sprite if self.sprite is not None else self.image
        screen.blit(surface, (draw_x, draw_y))
