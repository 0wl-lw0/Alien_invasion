import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Class for controlling a ship."""

    def __init__(self, ai_game):
        """Initialising ship and stand his start position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Download ship image and get rectangle.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Every new ship creating in down side of display
        self.rect.midbottom = self.screen_rect.midbottom

        # Saved amount coodinate in the center ship.
        self.x = float(self.rect.x)

        # Flag of remuving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Renew ship position with including flag."""
        # Renew attribute x, not rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.speedup_scale
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.speedup_scale

        # Renew attribute rect based self.x
        self.rect.x = self.x

    def blitme(self):
        """Drawing ship in current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Placing the ship in mid bottom side."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        