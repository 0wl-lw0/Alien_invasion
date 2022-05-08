class GameStats():
    """Initialising stats for game Alien Invasion."""

    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Game Alien Invasion starting in active stable.
        self.game_active = True

        # Game starts in inactive stable.
        self.game_active = False

        # Score don't renew.
        self.high_score = 0


    def reset_stats(self):
        """Initialising statistics, changing duration in game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
