"""Tests for Game class and GameState enum."""

import pygame
import pytest

from blades_of_the_fallen_realm.engine.game import Game, GameState


@pytest.fixture
def game() -> Game:
    """Provide a Game instance for each test."""
    return Game()


def test_game_state_enum_values() -> None:
    """Verify GameState enum has all required states."""
    assert GameState.MENU.value == "MENU"
    assert GameState.CHARACTER_SELECT.value == "CHARACTER_SELECT"
    assert GameState.PLAYING.value == "PLAYING"
    assert GameState.CAMP.value == "CAMP"
    assert GameState.PAUSED.value == "PAUSED"
    assert GameState.GAME_OVER.value == "GAME_OVER"


def test_game_initial_state(game: Game) -> None:
    """Test that game initializes with MENU state."""
    assert game.state == GameState.MENU


def test_game_initial_players_list(game: Game) -> None:
    """Test that game initializes with empty players list."""
    assert game.players == []
    assert isinstance(game.players, list)


def test_game_clock_exists(game: Game) -> None:
    """Test that game has a pygame clock."""
    assert isinstance(game.clock, pygame.time.Clock)


def test_change_state_to_character_select(game: Game) -> None:
    """Test changing state from MENU to CHARACTER_SELECT."""
    game.change_state(GameState.CHARACTER_SELECT)
    assert game.state == GameState.CHARACTER_SELECT


def test_change_state_to_playing(game: Game) -> None:
    """Test changing state to PLAYING."""
    game.change_state(GameState.PLAYING)
    assert game.state == GameState.PLAYING


def test_change_state_to_camp(game: Game) -> None:
    """Test changing state to CAMP."""
    game.change_state(GameState.CAMP)
    assert game.state == GameState.CAMP


def test_change_state_to_paused(game: Game) -> None:
    """Test changing state to PAUSED."""
    game.change_state(GameState.PAUSED)
    assert game.state == GameState.PAUSED


def test_change_state_to_game_over(game: Game) -> None:
    """Test changing state to GAME_OVER."""
    game.change_state(GameState.GAME_OVER)
    assert game.state == GameState.GAME_OVER


def test_state_transitions_sequence(game: Game) -> None:
    """Test a sequence of state transitions."""
    assert game.state == GameState.MENU

    game.change_state(GameState.CHARACTER_SELECT)
    assert game.state == GameState.CHARACTER_SELECT

    game.change_state(GameState.PLAYING)
    assert game.state == GameState.PLAYING

    game.change_state(GameState.PAUSED)
    assert game.state == GameState.PAUSED

    game.change_state(GameState.PLAYING)
    assert game.state == GameState.PLAYING

    game.change_state(GameState.CAMP)
    assert game.state == GameState.CAMP

    game.change_state(GameState.PLAYING)
    assert game.state == GameState.PLAYING

    game.change_state(GameState.GAME_OVER)
    assert game.state == GameState.GAME_OVER


def test_add_player_single(game: Game) -> None:
    """Test adding a single player."""

    # Create a mock player object
    class MockPlayer:
        pass

    player1 = MockPlayer()
    game.add_player(player1)

    assert len(game.players) == 1
    assert game.players[0] is player1


def test_add_player_two_players(game: Game) -> None:
    """Test adding two players for co-op."""

    # Create mock player objects
    class MockPlayer:
        pass

    player1 = MockPlayer()
    player2 = MockPlayer()

    game.add_player(player1)
    game.add_player(player2)

    assert len(game.players) == 2
    assert game.players[0] is player1
    assert game.players[1] is player2


def test_players_list_is_always_list(game: Game) -> None:
    """Test that players is always a list type."""
    assert isinstance(game.players, list)

    class MockPlayer:
        pass

    game.add_player(MockPlayer())
    assert isinstance(game.players, list)

    game.add_player(MockPlayer())
    assert isinstance(game.players, list)


def test_update_method_exists(game: Game) -> None:
    """Test that update method can be called with delta time."""
    # Should not raise an exception
    game.update(0.016)  # ~60 FPS delta time
    game.update(1.0 / 60.0)


def test_draw_method_exists(game: Game) -> None:
    """Test that draw method can be called with a surface."""
    screen = pygame.Surface((960, 540))
    # Should not raise an exception
    game.draw(screen)
