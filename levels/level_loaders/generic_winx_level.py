import pygame
from pygame import *

from lib import *
from levels import *


class GenericWinxLevel(Level):
    def __init__(
            self,
            layout: Layout,
            level_file: str,
            velocity_movement=4,
            velocity_jump=4,
            velocity_fly=1,
            velocity_fly_max=12,
            num_players: int = 0
    ):
        super().__init__(
            layout,
            level_file,
            velocity_movement,
            velocity_jump,
            velocity_fly,
            velocity_fly_max,
            num_players
        )

    def success_animation(self):
        print("[GenericWinxLevel] success_animation")
        image_file = "images/winx_raw/winx-club-wallpaper_01.jpg"
        temp = pygame.image.load(image_file)
        x = temp.get_rect().size[0]
        y = temp.get_rect().size[1]
        diff = 0.4
        factor = (1.0-diff) * (self.layout.game_h / y)
        temp = pygame.transform.scale(temp, (int(round(factor * x)), int(round(factor * y))))

        # screen.fill(Color("#FFFFFF"))
        self.layout.screen_game.fill(Color("#000000"))
        pygame.draw.rect(
            self.layout.screen_game,
            Color("#FFFFFF"),
            (
                int(round(0.50 * self.layout.game_w - temp.get_rect().size[0] / 2)),
                int(round(diff * self.layout.game_h - (diff * self.layout.game_h) / 4)),
                temp.get_rect().size[0],
                temp.get_rect().size[1]
            )
        )
        self.layout.screen_game.blit(temp, (int(round(0.50 * self.layout.game_w - temp.get_rect().size[0] / 2)), int(round(diff * self.layout.game_h - (diff * self.layout.game_h) / 4))))

        pg_print_message(self.layout, "Muy bien!!!", int(round(self.layout.game_w / 5)), int(round(self.layout.game_h / 6)), size=64)

        self.layout.update()
        pygame.time.wait(5000)


