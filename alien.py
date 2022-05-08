import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class, representing one alien."""

    def __init__(self, ai_game):
        """Initialise alien and set his start position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Download alien image and set attribute rect.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Every new alien appear in left-up side of display.
        # self.rect.x = self.rect.widht
        # self.rect.y = self.rect.height

        # Saved exsact horizontal alien position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True, if alien stay in endge display"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Turning alien in right or left side."""
        self.x += (self.settings.alien_speed * \
                        self.settings.fleet_direction)
        self.rect.x = self.x
