import pygame
from pygame import *

from levels import Level
from lib import *
from entities import constants
from .platformblock import PlatformBlock


def draw_procedural_simple(TILE_X, TILE_Y):
    temp = Surface((TILE_X, TILE_Y))
    temp.convert()
    temp.fill(Color("#99ff99"))
    return temp


def draw_procedural(TILE_X, TILE_Y):
    bessel_perc = 8
    color_dark = "#b3b300"
    color_light = "#e6e600"
    color_main = "#ffff99"

    temp = create_block_bessel(
        TILE_X,
        TILE_Y,
        color_dark, color_light, color_main,
        bessel_perc)

    return temp


class GoalBlock(PlatformBlock):

    collides = True
    has_grip = False

    def __init__(self, level_loaded: Level, x, y):
        PlatformBlock.__init__(self, level_loaded, x, y)
        self.image = draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)
