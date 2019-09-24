import pygame
from pygame import *
import numpy as np

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


def draw_player(TILE_X, TILE_Y, bg_color, image_file=None, flip=False):
    temp_image = Surface((TILE_X, TILE_Y))
    if image_file is not None:
        temp = pygame.image.load(image_file)
        if flip:
            temp = pygame.transform.flip(temp, True, False)
        temp = pygame.transform.scale(temp, (TILE_X, TILE_Y))
        temp_image = temp   # without background
    else:
        temp_image.fill(Color(bg_color))
    temp_image.convert()
    return temp_image


class Ghost(Entity):

    collides = True
    has_grip = False
    transformed = False

    def __init__(
            self,
            level_loaded: Level,
            x, y, name,
            bg_color="#000000",
            image_file=None,
            image_transform=None,
            flip=False,
            force_background=False,
            jump_sound=None
    ):
        Entity.__init__(self)
        self.collides = False
        self.has_grip = False
        self.item = False
        self.collectable = False
        self.transformed = False
        self.fly = False

        self.level_loaded = level_loaded
        self.name = name
        self.bg_color = bg_color
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onStairs = False
        self.onBar = False
        self.on_goal = False
        self.image_file = image_file
        self.image_right = draw_player(
            level_loaded.TILE_X, level_loaded.TILE_Y,
            self.bg_color, image_file, True
        )
        self.image_left = draw_player(
            level_loaded.TILE_X, level_loaded.TILE_Y,
            self.bg_color, image_file, False
        )
        self.image = self.image_right
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

    def update(self, platforms, players):

        min_dist = np.inf
        for p1 in players:
            dist1 = (self.rect.left - p1.rect.left) ** 2 + (self.rect.top - p1.rect.top) ** 2
            if dist1 < min_dist:
                p = p1
                min_dist = dist1

        if abs(self.rect.left - p.rect.left)<10:
            self.xvel = 0
        else:
            self.xvel = -sign(self.rect.left - p.rect.left) * self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        if abs(self.rect.top - p.rect.top)<10:
            self.yvel = 0
        else:
            self.yvel = -sign(self.rect.top - p.rect.top) * self.level_loaded.ENEMY_VELOCITY_MOVEMENT

        if self.xvel > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.rect.top += self.yvel
