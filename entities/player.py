import pygame
from pygame import *

from entities import constants
from entities import Entity
from entities import PlatformBlock
from entities import StairsBlock
from entities import BarBlock
from entities import GoalBlock
from entities import GoalBlockLeft
from entities import GoalBlockRight
from entities import StarItem
from levels import Level


def draw_player(level_loaded: Level, color, image_file=None, flip=False, force_background=False):
    temp_image = Surface((level_loaded.TILE_X, level_loaded.TILE_Y))
    temp_image.fill(Color(color))
    if image_file is not None:
        temp = pygame.image.load(image_file)
        if flip:
            temp = pygame.transform.flip(temp, True, False)
        temp = pygame.transform.scale(temp, (level_loaded.TILE_X, level_loaded.TILE_Y))
        temp_image.blit(temp, [0, 0])
        if level_loaded.TILE_X > 16 and not force_background:
            temp_image = temp   # without background
    temp_image.convert()
    return temp_image


class Player(Entity):

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
        self.name = name
        self.level_loaded = level_loaded
        self.color = color
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onStairs = False
        self.onBar = False
        self.on_goal = False
        self.image = draw_player(level_loaded, self.color, image_file, flip, force_background)
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

    def update(self, up, down, left, right, platforms):
        if self.onStairs:
            self.yvel = 0
            if up: self.yvel = -self.level_loaded.VELOCITY_MOVEMENT
            if down: self.yvel = self.level_loaded.VELOCITY_MOVEMENT
        if self.onBar and down:
            self.yvel = self.level_loaded.VELOCITY_MOVEMENT
        if self.onGround and up:
            # only jump if on the ground
            self.jump_sound.play()
            self.yvel -= self.level_loaded.VELOCITY_JUMP

        if self.transformed and up and self.yvel > -self.level_loaded.VELOCITY_FLY_MAX:
            self.yvel -= self.level_loaded.VELOCITY_FLY
        if self.transformed and down and self.yvel < self.level_loaded.VELOCITY_FLY_MAX:
            self.yvel += self.level_loaded.VELOCITY_FLY

        if not self.onGround and not self.onStairs and not self.onBar:
            # only accelerate with gravity if in the air
            self.yvel += self.level_loaded.GRAVITY
            # max falling speed
            if self.yvel > self.level_loaded.VELOCITY_FALL_MAX:
                self.yvel = self.level_loaded.VELOCITY_FALL_MAX

        if left:
            self.xvel = -self.level_loaded.VELOCITY_MOVEMENT
        if right:
            self.xvel = self.level_loaded.VELOCITY_MOVEMENT
        if not(left or right):
            self.xvel = 0
        if not(up or down) and self.onStairs and self.onBar:
            self.yvel = 0

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, up, down, left, right, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # do y-axis collisions
        self.collide(0, self.yvel, up, down, left, right, platforms)

    def collide(self, xvel, yvel, up, down, left, right, platforms):

        any_stairs = False
        any_bar = False
        self.onGround = False
        if isinstance(self, Player):
            self.on_goal = False

        for p in platforms:

            if isinstance(self, Player) and (isinstance(p, GoalBlock) or isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight)):
                offset = 1
                self.rect.top += offset
                if pygame.sprite.collide_rect(self, p) and self.yvel >= 0:
                    self.on_goal = True
                self.rect.top -= offset

            if pygame.sprite.collide_rect(self, p) and p is not self:

                if yvel > 0 and (
                        isinstance(p, PlatformBlock)
                        or isinstance(p, GoalBlock)
                ):
                    self.onGround = True
                if isinstance(p, StairsBlock):
                    any_stairs = True
                if isinstance(p, BarBlock):
                    any_bar = True

                if isinstance(p, StarItem):
                    if not self.transformed:
                        self.transform()
                    self.transformed = True

                if xvel > 0 and p.collides:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                if xvel < 0 and p.collides:
                    self.rect.left = p.rect.right
                    self.xvel = 0

                if yvel > 0 and p.collides:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if yvel < 0 and p.collides:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                if yvel > 0 and p.has_grip and not (self.onStairs or self.onBar) and not down:
                    # this is like a collision since we are not moving
                    self.rect.bottom = p.rect.top
                    self.yvel = 0

        if not any_bar and self.onBar and yvel < 0:
            self.yvel = 1

        self.onStairs = any_stairs
        self.onBar = any_bar
