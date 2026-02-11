"""Tests for Player — combos, magic, mount/dismount, lives, score."""

from unittest.mock import patch

import pygame
import pytest

from blades_of_the_fallen_realm.engine.input_handler import InputHandler, P1_CONTROLS
from blades_of_the_fallen_realm.entities.base_entity import BaseEntity
from blades_of_the_fallen_realm.entities.player import Player
from blades_of_the_fallen_realm.settings import (
    COMBO_WINDOW_MS,
    INVINCIBILITY_FRAMES,
    STARTING_LIVES,
)

# ---------------------------------------------------------------------------
# Construction / properties
# ---------------------------------------------------------------------------


def test_player_inherits_from_base_entity() -> None:
    """Player should be a subclass of BaseEntity."""
    player = Player()
    assert isinstance(player, BaseEntity)


def test_player_default_properties() -> None:
    """Player should have correct default properties."""
    player = Player(x=10.0, y=20.0, player_id=1)
    assert player.player_id == 1
    assert player.lives == STARTING_LIVES
    assert player.score == 0
    assert player.combo_count == 0
    assert player.is_mounted is False
    assert player.palette_swap is False


def test_player_id_2_palette_swap() -> None:
    """Player 2 should have palette_swap enabled."""
    player = Player(player_id=2)
    assert player.player_id == 2
    assert player.palette_swap is True


def test_player_position() -> None:
    """Player position should be set correctly."""
    player = Player(x=50.0, y=100.0)
    assert player.x == 50.0
    assert player.y == 100.0


# ---------------------------------------------------------------------------
# 3-hit combo chain
# ---------------------------------------------------------------------------


def test_combo_chain_advances_correctly() -> None:
    """execute_combo() should advance ATTACK1 → ATTACK2 → ATTACK3."""
    player = Player()

    with patch("pygame.time.get_ticks", return_value=0):
        player.execute_combo()
    assert player.combo_count == 1
    assert player.state == "ATTACK1"

    with patch("pygame.time.get_ticks", return_value=100):
        player.execute_combo()
    assert player.combo_count == 2
    assert player.state == "ATTACK2"

    with patch("pygame.time.get_ticks", return_value=200):
        player.execute_combo()
    assert player.combo_count == 3
    assert player.state == "ATTACK3"


def test_combo_resets_when_timing_window_expires() -> None:
    """Combo should reset to ATTACK1 when COMBO_WINDOW_MS elapses."""
    player = Player()

    with patch("pygame.time.get_ticks", return_value=0):
        player.execute_combo()
    assert player.combo_count == 1
    assert player.state == "ATTACK1"

    # Exceed the combo window
    with patch("pygame.time.get_ticks", return_value=COMBO_WINDOW_MS + 1):
        player.execute_combo()
    assert player.combo_count == 1
    assert player.state == "ATTACK1"


def test_third_hit_causes_knockdown_state() -> None:
    """Third combo hit should set state to ATTACK3 (knockdown)."""
    player = Player()

    with patch("pygame.time.get_ticks", return_value=0):
        player.execute_combo()
    with patch("pygame.time.get_ticks", return_value=100):
        player.execute_combo()
    with patch("pygame.time.get_ticks", return_value=200):
        player.execute_combo()

    assert player.state == "ATTACK3"
    assert player.combo_count == 3


def test_combo_resets_after_third_hit() -> None:
    """After the 3rd hit, next combo should start fresh."""
    player = Player()

    with patch("pygame.time.get_ticks", return_value=0):
        player.execute_combo()
    with patch("pygame.time.get_ticks", return_value=100):
        player.execute_combo()
    with patch("pygame.time.get_ticks", return_value=200):
        player.execute_combo()
    assert player.combo_count == 3

    # Next combo within window should reset due to combo_count >= 3
    with patch("pygame.time.get_ticks", return_value=300):
        player.execute_combo()
    assert player.combo_count == 1
    assert player.state == "ATTACK1"


# ---------------------------------------------------------------------------
# Jump attack
# ---------------------------------------------------------------------------


def test_jump_attack_while_airborne() -> None:
    """Attacking while airborne should set state to JUMP_ATTACK."""
    handler = InputHandler(player_id=1, controls=P1_CONTROLS)
    player = Player(input_handler=handler)

    # Simulate being airborne
    player.z = 50.0

    # Simulate just pressing attack
    handler.just_pressed["ATTACK"] = True

    player.handle_input()
    assert player.state == "JUMP_ATTACK"


# ---------------------------------------------------------------------------
# Magic activation
# ---------------------------------------------------------------------------


def test_magic_tier1_with_1_shard() -> None:
    """1 shard should activate MAGIC_TIER1."""
    player = Player()
    player.magic_charges = 1
    player.activate_magic()
    assert player.state == "MAGIC_TIER1"
    assert player.magic_charges == 0


def test_magic_tier1_with_2_shards() -> None:
    """2 shards should activate MAGIC_TIER1."""
    player = Player()
    player.magic_charges = 2
    player.activate_magic()
    assert player.state == "MAGIC_TIER1"
    assert player.magic_charges == 0


def test_magic_tier2_with_3_shards() -> None:
    """3 shards should activate MAGIC_TIER2."""
    player = Player()
    player.magic_charges = 3
    player.activate_magic()
    assert player.state == "MAGIC_TIER2"
    assert player.magic_charges == 0


def test_magic_tier2_with_4_shards() -> None:
    """4 shards should activate MAGIC_TIER2."""
    player = Player()
    player.magic_charges = 4
    player.activate_magic()
    assert player.state == "MAGIC_TIER2"
    assert player.magic_charges == 0


def test_magic_tier3_with_5_shards() -> None:
    """5 shards should activate MAGIC_TIER3."""
    player = Player()
    player.magic_charges = 5
    player.activate_magic()
    assert player.state == "MAGIC_TIER3"
    assert player.magic_charges == 0


def test_magic_tier3_with_9_shards() -> None:
    """9 shards should activate MAGIC_TIER3."""
    player = Player()
    player.magic_charges = 9
    player.activate_magic()
    assert player.state == "MAGIC_TIER3"
    assert player.magic_charges == 0


def test_magic_activation_consumes_all_shards() -> None:
    """activate_magic() should consume all magic charges."""
    player = Player()
    player.magic_charges = 7
    player.activate_magic()
    assert player.magic_charges == 0


def test_magic_no_shards_does_nothing() -> None:
    """activate_magic() with 0 shards should not change state."""
    player = Player()
    player.magic_charges = 0
    player.activate_magic()
    assert player.state == "IDLE"
    assert player.magic_charges == 0


# ---------------------------------------------------------------------------
# Lives / respawn
# ---------------------------------------------------------------------------


def test_lives_decrement_on_respawn() -> None:
    """respawn() should decrement lives by 1."""
    player = Player()
    initial_lives = player.lives
    player.respawn()
    assert player.lives == initial_lives - 1


def test_respawn_resets_position() -> None:
    """respawn() should reset player to spawn position."""
    player = Player(x=100.0, y=200.0)
    player.x = 500.0
    player.y = 300.0
    player.z = 50.0
    player.respawn()
    assert player.x == 100.0
    assert player.y == 200.0
    assert player.z == 0.0


def test_respawn_grants_invincibility() -> None:
    """respawn() should grant invincibility frames."""
    player = Player()
    player.invincibility_frames = 0
    player.respawn()
    assert player.invincibility_frames == INVINCIBILITY_FRAMES


def test_respawn_restores_hp() -> None:
    """respawn() should restore HP to max."""
    player = Player()
    player.hp = 0
    player.respawn()
    assert player.hp == player.max_hp


def test_respawn_resets_state_and_combo() -> None:
    """respawn() should reset state to IDLE and combo count to 0."""
    player = Player()
    player.state = "ATTACK2"
    player.combo_count = 2
    player.respawn()
    assert player.state == "IDLE"
    assert player.combo_count == 0


# ---------------------------------------------------------------------------
# Score tracking
# ---------------------------------------------------------------------------


def test_add_score_increments() -> None:
    """add_score() should increment the score counter."""
    player = Player()
    player.add_score(100)
    assert player.score == 100


def test_add_score_accumulates() -> None:
    """add_score() should accumulate across multiple calls."""
    player = Player()
    player.add_score(100)
    player.add_score(250)
    player.add_score(50)
    assert player.score == 400


def test_add_score_zero() -> None:
    """add_score(0) should not change score."""
    player = Player()
    player.add_score(0)
    assert player.score == 0


# ---------------------------------------------------------------------------
# Mount / dismount
# ---------------------------------------------------------------------------


def test_mount_changes_state() -> None:
    """mount() should set is_mounted and state to MOUNT."""
    player = Player()
    mount_entity = BaseEntity()
    player.mount(mount_entity)
    assert player.is_mounted is True
    assert player.state == "MOUNT"


def test_dismount_restores_state() -> None:
    """dismount() should clear is_mounted and set state to IDLE."""
    player = Player()
    mount_entity = BaseEntity()
    player.mount(mount_entity)
    player.dismount()
    assert player.is_mounted is False
    assert player.state == "IDLE"


def test_mount_dismount_full_cycle() -> None:
    """Full mount → dismount cycle should transition states correctly."""
    player = Player()
    mount_entity = BaseEntity()

    assert player.is_mounted is False
    assert player.state == "IDLE"

    player.mount(mount_entity)
    assert player.is_mounted is True
    assert player.state == "MOUNT"

    player.dismount()
    assert player.is_mounted is False
    assert player.state == "IDLE"


# ---------------------------------------------------------------------------
# Handle input edge cases
# ---------------------------------------------------------------------------


def test_handle_input_no_handler() -> None:
    """handle_input() should do nothing when input_handler is None."""
    player = Player(input_handler=None)
    player.handle_input()
    assert player.state == "IDLE"


def test_handle_input_not_alive_player() -> None:
    """handle_input() should do nothing when player is not alive."""
    handler = InputHandler(player_id=1, controls=P1_CONTROLS)
    player = Player(input_handler=handler)
    player.hp = 0
    handler.just_pressed["ATTACK"] = True
    player.handle_input()
    assert player.state == "IDLE"
