"""Smoke tests for main.py and __main__.py entry points."""

from unittest.mock import MagicMock, patch

import pygame


def test_main_module_importable() -> None:
    """main.py module should be importable without side effects."""
    from blades_of_the_fallen_realm import main

    assert hasattr(main, "main")


def test_main_function_is_callable() -> None:
    """main() function should be callable."""
    from blades_of_the_fallen_realm.main import main

    assert callable(main)


@patch("blades_of_the_fallen_realm.main.sys")
@patch("blades_of_the_fallen_realm.main.pygame")
def test_main_initializes_pygame(mock_pygame: MagicMock, mock_sys: MagicMock) -> None:
    """main() should call pygame.init() and set_mode() with correct settings."""
    from blades_of_the_fallen_realm.main import main
    from blades_of_the_fallen_realm.settings import (
        FPS,
        GAME_TITLE,
        SCREEN_HEIGHT,
        SCREEN_WIDTH,
    )

    # Make event.get return a QUIT event so the loop exits immediately
    quit_event = MagicMock()
    quit_event.type = pygame.QUIT
    mock_pygame.QUIT = pygame.QUIT
    mock_pygame.event.get.return_value = [quit_event]

    main()

    mock_pygame.init.assert_called_once()
    mock_pygame.display.set_mode.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT))
    mock_pygame.display.set_caption.assert_called_once_with(GAME_TITLE)
    mock_pygame.quit.assert_called_once()


def test_dunder_main_importable() -> None:
    """__main__.py should be importable (the main() call is at module level)."""
    import importlib.util

    # We can't actually run __main__.py as it calls main() at import time.
    # Instead, verify the module file exists and is loadable by checking spec.
    spec = importlib.util.find_spec("blades_of_the_fallen_realm.__main__")
    assert spec is not None
