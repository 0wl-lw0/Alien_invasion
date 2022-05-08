class Settings():
    """Class for collecting all settings for game Alien Invasion."""

    def __init__(self):
        """Initialising settings of game."""
        # Display parametr
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1
        self.ship_limit = 3
        
        # Parameters of bullet
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (123, 60, 255)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 15

        # Boosting game every lvl-up.
        self.speedup_scale = 1.1
        # Tempo increase cost of aliens
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings, changing in the game session"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        # fleet_direction = 1 mean going in right; and -1 - in left.
        self.fleet_direction = 1

        # Count score
        self.alien_points = 50

    def increase_speed(self):
        """Increasing settings of speed and alien cost."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
