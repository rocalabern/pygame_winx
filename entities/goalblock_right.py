import pygame
from pygame import *

from levels import Level
from lib import *
from entities import constants
from .platformblock import PlatformBlock


class GoalBlockRight(PlatformBlock):

    image_empty = "images/sprites/HUD/hudHeart_empty.png"
    image_full = "images/sprites/HUD/hudHeart_full.png"

    def __init__(self, level_loaded: Level, x, y):
        PlatformBlock.__init__(self, level_loaded, x, y)
        self.collides = True
        self.has_grip = False
        self.item = False
        self.collectable = False
        self.transformed = False
        self.fly = False

        self.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, self.image_empty)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)

    def set_draw_procedural(self, TILE_X, TILE_Y, image_file):
        bessel_perc = 8
        color_dark = "#b3b300"
        color_light = "#e6e600"
        color_main = "#ffff99"

        temp = create_block_bessel_right(
            TILE_X,
            TILE_Y,
            color_dark, color_light, color_main,
            bessel_perc)

        flip = False
        temp_image = pygame.image.load(image_file)
        if flip:
            temp_image = pygame.transform.flip(temp_image, True, False)
        temp_image = pygame.transform.scale(temp_image, (TILE_X, TILE_Y))
        temp.blit(temp_image, [-TILE_X//2, 0])

        self.image = temp
