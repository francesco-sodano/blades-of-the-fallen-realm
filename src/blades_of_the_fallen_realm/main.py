"""Blades of the Fallen Realm — Entry point.

A retro side-scrolling beat 'em up inspired by SEGA Golden Axe (1989).
"""

import sys

import pygame

from blades_of_the_fallen_realm.settings import (
    FPS,
    GAME_TITLE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


def main() -> None:
    """Initialize PyGame and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
