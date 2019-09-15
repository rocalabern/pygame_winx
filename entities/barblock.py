import pygame
from pygame import *

from entities import constants
from levels import Level
from .entity import Entity


def draw_procedural(TILE_X, TILE_Y):
    temp = Surface((TILE_X, TILE_Y))
    temp.convert()
    temp.fill(Color(constants.COLOR_BAR_BCKGRND), Rect(0, 0, TILE_X, TILE_Y))
    # temp.fill(Color(constants.COLOR_BAR), Rect(0, 0, constants.TILE_X, 2))
    COLOR_BAR_LIGHT = "#f5f5f0"
    COLOR_BAR = "#adad85"
    COLOR_BAR_DARK = "#5c5c3d"
    if TILE_Y < 32:
        temp.fill(Color(COLOR_BAR_LIGHT), Rect(0, 0, TILE_X, 1))
        temp.fill(Color(COLOR_BAR), Rect(0, 1, TILE_X, 1))
        temp.fill(Color(COLOR_BAR_DARK), Rect(0, 2, TILE_X, 1))
    else:
        temp.fill(Color(COLOR_BAR_LIGHT), Rect(0, 0, TILE_X, 2))
        temp.fill(Color(COLOR_BAR), Rect(0, 2, TILE_X, 2))
        temp.fill(Color(COLOR_BAR_DARK), Rect(0, 4, TILE_X, 2))

    return temp


class BarBlock(Entity):

    collides = False
    has_grip = True

    def __init__(self, level_loaded: Level, x, y):
        Entity.__init__(self)
        self.image = draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)
