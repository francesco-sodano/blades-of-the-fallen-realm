"""Shared pytest fixtures for Blades of the Fallen Realm tests."""

import pytest
import pygame

from blades_of_the_fallen_realm.engine.camera import Camera
from blades_of_the_fallen_realm.engine.game import Game
from blades_of_the_fallen_realm.engine.input_handler import (
    InputHandler,
    P1_CONTROLS,
    P2_CONTROLS,
)
from blades_of_the_fallen_realm.engine.renderer import Renderer
from blades_of_the_fallen_realm.entities.base_entity import BaseEntity


@pytest.fixture(autouse=True, scope="session")
def init_pygame() -> None:  # type: ignore[misc]
    """Initialize pygame once for the entire test session."""
    pygame.init()
    yield  # type: ignore[misc]
    pygame.quit()


@pytest.fixture
def screen() -> pygame.Surface:
    """Provide a test pygame display surface.

    This fixture creates a 960x540 pygame Surface for UI and rendering tests.
    Currently used minimally as most tests focus on logic rather than rendering.
    Intended for future UI tests, menu rendering tests, and HUD component tests.
    """
    return pygame.Surface((960, 540))


@pytest.fixture
def base_entity() -> BaseEntity:
    """Provide a BaseEntity instance with default position."""
    return BaseEntity(x=100.0, y=200.0)


@pytest.fixture
def renderer() -> Renderer:
    """Provide an empty Renderer instance."""
    return Renderer()


@pytest.fixture
def camera() -> Camera:
    """Provide a Camera instance."""
    return Camera()


@pytest.fixture
def input_handler_p1() -> InputHandler:
    """Provide a Player 1 InputHandler instance."""
    return InputHandler(player_id=1, controls=P1_CONTROLS)


@pytest.fixture
def input_handler_p2() -> InputHandler:
    """Provide a Player 2 InputHandler instance."""
    return InputHandler(player_id=2, controls=P2_CONTROLS)


@pytest.fixture
def game() -> Game:
    """Provide a Game instance."""
    return Game()
