"""Shared pytest fixtures for Blades of the Fallen Realm tests."""

import pytest
import pygame


@pytest.fixture(autouse=True, scope="session")
def init_pygame() -> None:  # type: ignore[misc]
    """Initialize pygame once for the entire test session."""
    pygame.init()
    yield  # type: ignore[misc]
    pygame.quit()


@pytest.fixture
def screen() -> pygame.Surface:
    """Provide a test pygame display surface."""
    return pygame.Surface((960, 540))


@pytest.fixture
def base_entity() -> "BaseEntity":  # type: ignore[name-defined]  # noqa: F821
    """Provide a BaseEntity instance with default position."""
    from blades_of_the_fallen_realm.entities.base_entity import BaseEntity

    return BaseEntity(x=100.0, y=200.0)


@pytest.fixture
def renderer() -> "Renderer":  # type: ignore[name-defined]  # noqa: F821
    """Provide an empty Renderer instance."""
    from blades_of_the_fallen_realm.engine.renderer import Renderer

    return Renderer()


@pytest.fixture
def camera() -> "Camera":  # type: ignore[name-defined]  # noqa: F821
    """Provide a Camera instance with default level width."""
    from blades_of_the_fallen_realm.engine.camera import Camera

    return Camera(level_width=4000)


@pytest.fixture
def input_handler_p1() -> "InputHandler":  # type: ignore[name-defined]  # noqa: F821
    """Provide a Player 1 InputHandler instance."""
    from blades_of_the_fallen_realm.engine.input_handler import (
        InputHandler,
        P1_CONTROLS,
    )

    return InputHandler(player_id=1, controls=P1_CONTROLS)


@pytest.fixture
def game() -> "Game":  # type: ignore[name-defined]  # noqa: F821
    """Provide a Game instance."""
    from blades_of_the_fallen_realm.engine.game import Game

    return Game()
