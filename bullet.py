import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for bullets controll, shooting a ship."""

    def __init__(self, ai_game):
        """Creating bullet object in the current ship position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creating bullet in position (0, 0) and appointment right position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Bullet position save in real format.
        self.y = float(self.rect.y)


    def update(self):
        """Replacing bullets to up on display."""
        # Renew bullet position in real format.
        self.y -= self.settings.bullet_speed

        # Renew position rectangle
        self.rect.y = self.y


    def draw_bullet(self):
        """Print bullet on display."""
        pygame.draw.rect(self.screen, self.color, self.rect)