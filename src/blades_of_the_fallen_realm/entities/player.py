"""Player character logic — combos, jump attack, throw, magic, mount/dismount, lives."""

from __future__ import annotations

import pygame

from blades_of_the_fallen_realm.engine.input_handler import InputHandler
from blades_of_the_fallen_realm.entities.base_entity import BaseEntity
from blades_of_the_fallen_realm.settings import (
    COMBO_WINDOW_MS,
    INVINCIBILITY_FRAMES,
    STARTING_LIVES,
    WALK_SPEED,
)

# Combo chain states in order
_COMBO_STATES: list[str] = ["ATTACK1", "ATTACK2", "ATTACK3"]


class Player(BaseEntity):
    """Player-controlled character with combos, magic, mounts, and lives.

    Inherits from :class:`BaseEntity` and adds player-specific features:
    combo chains, jump attacks, running attacks, throw, tiered magic,
    mount/dismount, lives, and score tracking.
    """

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        player_id: int = 1,
        input_handler: InputHandler | None = None,
    ) -> None:
        """Initialise a player entity.

        Args:
            x: Horizontal position in world space.
            y: Depth-axis position in world space (pseudo-3D Y).
            player_id: Player identifier (1 or 2).
            input_handler: Reference to the player's input handler.
        """
        super().__init__(x=x, y=y)

        # Identity
        self.player_id: int = player_id
        self.palette_swap: bool = player_id == 2

        # Lives & scoring
        self.lives: int = STARTING_LIVES
        self.score: int = 0

        # Combo tracking
        self.combo_count: int = 0
        self._last_attack_time: int = 0

        # Input
        self.input_handler: InputHandler | None = input_handler

        # Mount
        self.is_mounted: bool = False
        self._mount_entity: BaseEntity | None = None

        # Spawn position for respawn
        self._spawn_x: float = x
        self._spawn_y: float = y

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------

    def handle_input(self) -> None:
        """Process input handler state and dispatch actions.

        Reads direction, attack, jump, and magic inputs from the
        assigned :class:`InputHandler` and transitions the player's
        state accordingly.
        """
        if self.input_handler is None:
            return

        if not self.is_alive:
            return

        # Movement
        dx, dy = self.input_handler.get_direction()

        if dx != 0 or dy != 0:
            self.vel_x = dx * WALK_SPEED
            self.vel_y = dy * WALK_SPEED
            if dx > 0:
                self.facing = "right"
            elif dx < 0:
                self.facing = "left"
            if self.is_on_ground() and self.state not in _COMBO_STATES:
                self.change_state("WALK")
        else:
            self.vel_x = 0.0
            self.vel_y = 0.0
            if self.is_on_ground() and self.state not in _COMBO_STATES:
                self.change_state("IDLE")

        # Attack
        if self.input_handler.is_just_pressed("ATTACK"):
            if not self.is_on_ground():
                self.change_state("JUMP_ATTACK")
            else:
                self.execute_combo()

        # Jump
        if self.input_handler.is_just_pressed("JUMP") and self.is_on_ground():
            self.change_state("JUMP")

        # Magic
        if self.input_handler.is_just_pressed("MAGIC"):
            self.activate_magic()

    # ------------------------------------------------------------------
    # Combo system
    # ------------------------------------------------------------------

    def execute_combo(self) -> None:
        """Advance the combo chain or reset if the timing window expired.

        The chain follows ``ATTACK1 → ATTACK2 → ATTACK3``.  The third
        hit causes a *knockdown* state.  If the elapsed time since the
        last attack exceeds :data:`COMBO_WINDOW_MS` the chain resets to
        the first hit.
        """
        current_time: int = pygame.time.get_ticks()
        elapsed: int = current_time - self._last_attack_time

        if elapsed > COMBO_WINDOW_MS or self.combo_count >= 3:
            # Reset combo chain
            self.combo_count = 0

        # Advance to next hit in chain
        self.combo_count += 1
        self._last_attack_time = current_time

        state_index: int = min(self.combo_count, 3) - 1
        new_state: str = _COMBO_STATES[state_index]
        self.change_state(new_state)

        # Third hit causes knockdown (state already set via _COMBO_STATES)

    # ------------------------------------------------------------------
    # Magic system
    # ------------------------------------------------------------------

    def activate_magic(self) -> None:
        """Consume magic shards and trigger the appropriate magic tier.

        Tier mapping:

        * **1–2 shards** → tier 1 (``MAGIC_TIER1``)
        * **3–4 shards** → tier 2 (``MAGIC_TIER2``)
        * **5+ shards**  → tier 3 (``MAGIC_TIER3``)

        All current shards are consumed on activation.  Does nothing if
        the player has zero shards.
        """
        if self.magic_charges <= 0:
            return

        charges: int = self.magic_charges

        if charges >= 5:
            self.change_state("MAGIC_TIER3")
        elif charges >= 3:
            self.change_state("MAGIC_TIER2")
        else:
            self.change_state("MAGIC_TIER1")

        # Consume all shards
        self.magic_charges = 0

    # ------------------------------------------------------------------
    # Mount / dismount
    # ------------------------------------------------------------------

    def mount(self, mount_entity: BaseEntity) -> None:
        """Enter the MOUNT state and attach to a mount entity.

        Args:
            mount_entity: The mount entity to ride (e.g. Destrier, Snarlfang).
        """
        self.is_mounted = True
        self._mount_entity = mount_entity
        self.change_state("MOUNT")

    def dismount(self) -> None:
        """Exit the MOUNT state and restore normal controls."""
        self.is_mounted = False
        self._mount_entity = None
        self.change_state("IDLE")

    # ------------------------------------------------------------------
    # Lives & respawn
    # ------------------------------------------------------------------

    def respawn(self) -> None:
        """Decrement lives and reset position with invincibility.

        Resets the player to their spawn position, restores full HP,
        and grants invincibility frames.  If no lives remain the
        method still decrements (caller should check ``lives``
        before calling).
        """
        self.lives -= 1
        self.x = self._spawn_x
        self.y = self._spawn_y
        self.z = 0.0
        self.hp = self.max_hp
        self.invincibility_frames = INVINCIBILITY_FRAMES
        self.change_state("IDLE")
        self.combo_count = 0

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------

    def add_score(self, points: int) -> None:
        """Add points to the player's score counter.

        Args:
            points: Number of points to add.
        """
        self.score += points
