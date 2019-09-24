import pygame
from pygame import *

from levels import GameLevel
from levels.level_loaders import GenericWinxLevel
from lib import *


def main(width: int = None, height: int = None):
    pygame.mixer.pre_init(48000, -16, 2, 2048)
    pygame.init()
    pygame.display.set_caption("Winx Club")

    if width is None or height is None:
        # screen_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # screen_window = pygame.display.set_mode((800, 600))
        screen_window = pygame.display.set_mode((1280, 720))
    else:
        screen_window = pygame.display.set_mode((width, height))
    layout = Layout(screen_window, allow_rescale=True)

    levels_loaded = [
        # GenericWinxLevel(layout, "levels/level_txt/level_01.txt"),
        GenericWinxLevel(layout, "levels/level_txt/level_02.txt"),
        GenericWinxLevel(layout, "levels/level_txt/level_03.txt")
    ]

    done = False
    i = 0
    while i < len(levels_loaded) and not done:
        game_level = GameLevel(levels_loaded[i])
        game_level.play()
        i = i + 1


if __name__ == "__main__":
    main()
