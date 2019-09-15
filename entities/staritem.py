import pygame
from pygame import *

from entities import constants
from levels import Level
from .entity import Entity


def draw_sprite(TILE_X, TILE_Y):
    image_file = "images/sprites/items_collectables/star.png"
    temp = pygame.image.load(image_file)
    temp = pygame.transform.scale(temp, (TILE_X, TILE_Y))
    return temp


class StarItem(Entity):

    collides = False
    has_grip = False

    def __init__(self, level_loaded: Level, x, y):
        Entity.__init__(self)
        self.image = draw_sprite(level_loaded.TILE_X, level_loaded.TILE_Y)
        self.rect = Rect(x, y, level_loaded.TILE_X, level_loaded.TILE_Y)

