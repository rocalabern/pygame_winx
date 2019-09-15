import pygame
from pygame import *

from levels import Level
from lib import *

from entities import constants
from entities import Entity
from entities import PlatformBlock
from entities import StairsBlock
from entities import BarBlock
from entities import GoalBlock
from entities import GoalBlockLeft
from entities import GoalBlockRight
from entities import StarItem


def draw_player(TILE_X, TILE_Y, color, image_file=None, flip=False, force_background=False):
    temp_image = Surface((TILE_X, TILE_Y))
    temp = pygame.image.load('images/winx_raw/tritannus_01.png')
    if flip:
        temp = pygame.transform.flip(temp, True, False)
    temp = pygame.transform.scale(temp, (TILE_X, TILE_Y))
    temp_image = temp   # without background
    temp_image.convert()
    return temp_image


class Tritannus(Entity):

    collides = True
    has_grip = False
    transformed = False

    def __init__(
            self,
            level_loaded: Level,
            x, y, name,
            color="#000000",
            image_file=None,
            image_transform=None,
            flip=False,
            force_background=False,
            jump_sound=None
    ):
        Entity.__init__(self)
        self.level_loaded = level_loaded
        self.name = name
        self.color = color
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onStairs = False
        self.onBar = False
        self.on_goal = False
        self.image = draw_player(
            level_loaded.TILE_X, level_loaded.TILE_Y,
            self.color, image_file, flip, force_background
        )
        self.image_transform = image_transform
        self.rect = Rect(x, y, level_loaded.TILE_X-2, level_loaded.TILE_Y)
        if jump_sound is None:
            self.jump_sound = None
        else:
            self.jump_sound = pygame.mixer.Sound(jump_sound)
            self.jump_sound.set_volume(1.0)

    def transform(self, flip=False):
        temp_image = pygame.image.load(self.image_transform)
        if flip:
            temp_image = pygame.transform.flip(temp_image, True, False)
        temp_image = pygame.transform.scale(temp_image, (self.level_loaded.TILE_X, self.level_loaded.TILE_Y))
        temp_image.convert()
        self.image = temp_image

    def update(self, platforms, p1, p2):

        dist1 = (self.rect.left - p1.rect.left) ** 2 + (self.rect.top - p1.rect.top) ** 2
        dist2 = (self.rect.left - p2.rect.left) ** 2 + (self.rect.top - p2.rect.top) ** 2
        if dist1<dist2:
            p = p1
        else:
            p = p2

        self.xvel = -sign(self.rect.left - p.rect.left) * self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        self.yvel = -sign(self.rect.top - p.rect.top) * self.level_loaded.ENEMY_VELOCITY_MOVEMENT

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.rect.top += self.yvel
