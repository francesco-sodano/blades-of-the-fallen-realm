"""Game state manager — handles MENU, CHARACTER_SELECT, PLAYING, CAMP, PAUSED, GAME_OVER."""

from enum import Enum

import pygame

from blades_of_the_fallen_realm.entities.base_entity import BaseEntity


class GameState(str, Enum):
    """Game state enumeration using string values."""

    MENU = "MENU"
    CHARACTER_SELECT = "CHARACTER_SELECT"
    PLAYING = "PLAYING"
    CAMP = "CAMP"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


class Game:
    """Main game class managing state machine and game loop."""

    def __init__(self) -> None:
        """Initialize the game with default state and empty player list."""
        self.state: GameState = GameState.MENU
        self.players: list[BaseEntity] = []
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def change_state(self, new_state: GameState) -> None:
        """
        Transition to a new game state.

        Args:
            new_state: The target state to transition to.
        """
        self.state = new_state

    def add_player(self, player: BaseEntity) -> None:
        """
        Add a player to the game.

        Args:
            player: The player to add to the players list.
        """
        self.players.append(player)

    def update(self, dt: float) -> None:
        """
        Update game logic based on current state.

        Args:
            dt: Delta time in seconds since last frame.
        """
        # State-specific update logic will be delegated here
        # For now, this is a placeholder for state handler delegation
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the game based on current state.

        Args:
            screen: The pygame surface to draw on.
        """
        # State-specific drawing logic will be delegated here
        # For now, this is a placeholder for state handler delegation
        pass
