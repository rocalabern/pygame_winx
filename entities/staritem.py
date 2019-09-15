import pygame
from pygame import *

from entities import constants
from .entity import Entity


def draw_sprite():
    image_file = "images/sprites/items_collectables/star.png"
    temp = pygame.image.load(image_file)
    temp = pygame.transform.scale(temp, (constants.TILE_X, constants.TILE_Y))
    return temp


class StarItem(Entity):

    collides = False
    has_grip = False

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = draw_sprite()
        self.rect = Rect(x, y, constants.TILE_X, constants.TILE_Y)