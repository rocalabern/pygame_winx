import pygame
from pygame import *

from entities import constants
from levels import Level
from .entity import Entity


def draw_sprite(TILE_X, TILE_Y):
    image_file = "images/sprites/items/ladderMid.png"
    temp = pygame.image.load(image_file)
    temp = pygame.transform.scale(temp, (TILE_X, TILE_Y))
    return temp


def draw_procedural_simple(TILE_X, TILE_Y):
    temp = Surface((TILE_X, TILE_Y))
    temp.convert()
    temp.fill(Color(constants.COLOR_STAIRS_BCKGRND))
    for i_step in range(TILE_Y // 4):
        temp.fill(Color(constants.COLOR_STAIRS), Rect(0, 8 * i_step, TILE_X, 1))
    return temp


def draw_procedural(TILE_X, TILE_Y):
    COLOR_BAR_LIGHT = "#ffe699"
    COLOR_BAR = "#ffbf00"
    COLOR_BAR_DARK = "#b38600"
    temp = Surface((TILE_X, TILE_Y))
    temp.convert()
    temp.fill(Color(constants.COLOR_STAIRS_BCKGRND))
    i_step = 0
    while i_step <= TILE_Y:
        if TILE_Y<32:
            temp.fill(Color(COLOR_BAR_LIGHT), Rect(0, i_step, TILE_X, 1))
            temp.fill(Color(COLOR_BAR), Rect(0, i_step+1, TILE_X, 1))
            temp.fill(Color(COLOR_BAR_DARK), Rect(0, i_step+2, TILE_X, 1))
            i_step = i_step + 8
        else:
            temp.fill(Color(COLOR_BAR_LIGHT), Rect(0, i_step, TILE_X, 1))
            temp.fill(Color(COLOR_BAR), Rect(0, i_step+1, TILE_X, 2))
            temp.fill(Color(COLOR_BAR_DARK), Rect(0, i_step+3, TILE_X, 1))
            i_step = i_step + 8
    return temp

class StairsBlock(Entity):

    collides = False
    has_grip = True

    def __init__(self, level_loaded: Level, x, y):
        Entity.__init__(self)
        self.image = draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)

