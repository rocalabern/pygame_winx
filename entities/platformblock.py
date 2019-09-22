import pygame
from pygame import *

from levels import Level
from lib import *
from entities import constants
from .entity import Entity


def draw_sprite(tile_x, tile_y):
    image_file = "images/sprites/ground/stoneCenter.png"
    # image_file = "images/sprites/items/boxCrate.png"
    temp = pygame.image.load(image_file)
    temp = pygame.transform.scale(temp, (tile_x, tile_y))
    return temp


def draw_procedural_simple(tile_x, tile_y):
    temp = Surface((tile_x, tile_y))
    temp.convert()
    temp.fill(Color("#392613"))
    return temp


def draw_procedural(TILE_X, TILE_Y):
    bessel_perc = 8
    color_dark = "#a3a375"
    color_light = "#ebebe0"
    color_main = "#ccccb3"

    temp = create_block_bessel(
        TILE_X,
        TILE_Y,
        color_dark, color_light, color_main,
        bessel_perc)

    return temp


class PlatformBlock(Entity):

    def __init__(self, level_loaded: Level, x, y):
        Entity.__init__(self)
        self.collides = True
        self.has_grip = False
        self.item = False
        self.collectable = False
        self.transformed = False
        self.fly = False

        self.image = draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)
