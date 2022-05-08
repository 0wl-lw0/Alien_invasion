import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star

class AlienInvasion:
    """Class for controlling resourses and game condition."""


    def __init__(self):
        """Initialising game and create game resources."""
        pygame.init()
        # Initialising background color.
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_width = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Creating attribute for saving gaming statistics.
        # and panel of results.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # self.stars = pygame.sprite.Group()
        # self.star = Star(self)

        self._create_fleet()
        # self._create_stars()

        # Creating button Play.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Runing main loop of game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _check_events(self):
        """Tracking of events keyboard and mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Launch new game when you click Play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Clear game session
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Clear list aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Creating new fleet and placing the ship of center
            self._create_fleet()
            self.ship.center_ship()

            # Coursore is hidding
            pygame.mouse.set_visible(False)



    def _check_keydown_events(self, event):
        """Reacted for pressing keyword."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Reacted on letting keyword."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Creating new bullet and launch him in group bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Renew positions of bullets and kill old bullets."""
        # Renew positions of bullets.
        self.bullets.update()

        # Deleting bullets, over the edge display.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Checkin hitting of aliens.
        # When found hint del bullet and alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Deleting existing bullets and creating new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Level up
            self.stats.level += 1
            self.sb.prep_level()


    def _ship_hint(self):
        # Increase ships_left.
        if self.stats.ships_left > 0:
            # Uncrease ships_left and renew score pannel
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # clear list of aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Creating new fleet and placing the ship in center
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    
    def _update_aliens(self):
        """
        Check, stay fleet in edge of display or not,
        with than renew all positions of aliens in fleet. 
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Checking collisions "alien - ship"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._ship_hint()

        self._check_aliens_bottom()


    def _create_fleet(self):
        """Creating fleet invasion"""
        # Creating the alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Calculating number of rows, placing on display."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - \
            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_width)

        # Creting fleet of aliens invasion.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Creating an alien and replacing him in row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Reacted on achive of alien edge's display."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Changing way of fleet."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Checking, aliens in the end of side bottom."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Same thing, how like hit ship
                self._ship_hint()
                break


    def _update_screen(self):
        """Every time loop, display redraws."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # self.stars.draw(self.screen)
        self.sb.show_score()
        
        # Button Play showing if game active.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Showing last traced display.
        pygame.display.flip()



if __name__ == '__main__':
    # Creating instance and launch game.
    ai = AlienInvasion()
    ai.run_game()
