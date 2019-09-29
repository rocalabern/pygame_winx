import pygame
from pygame import *
import numpy as np

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
from lib import Dijkstra


def draw_player(level_loaded: Level, bg_color, image_file=None, flip=False, force_background=False):
    temp_image = Surface((level_loaded.TILE_X, level_loaded.TILE_Y))
    temp_image.fill(Color(bg_color))
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


class Enemy(Entity):

    collides = True
    has_grip = False
    transformed = False

    def __init__(
            self,
            level_loaded: Level,
            x, y, name,
            key_up,
            key_down,
            key_right,
            key_left,
            bg_color="#000000",
            image_file=None,
            image_transform=None,
            flip=False,
            force_background=False,
            jump_sound=None,
    ):
        Entity.__init__(self)
        self.collides = True
        self.has_grip = False
        self.item = False
        self.collectable = False
        self.transformed = False
        self.fly = False

        self.target_player = None
        self.path = None
        self.path_last_calc = pygame.time.get_ticks()

        self.name = name
        self.level_loaded = level_loaded

        self.key_up = key_up
        self.key_down = key_down
        self.key_right = key_right
        self.key_left = key_left

        self.key_pressed_up = False
        self.key_pressed_down = False
        self.key_pressed_left = False
        self.key_pressed_right = False

        self.bg_color = bg_color
        self.vel_x = 0
        self.vel_y = 0
        self.onGround = False
        self.onStairs = False
        self.onBar = False
        self.on_goal = False
        self.image = draw_player(level_loaded, self.bg_color, image_file, flip, force_background)
        self.image_transform = image_transform
        self.rect = Rect(x, y, level_loaded.TILE_X-2, level_loaded.TILE_Y)
        if jump_sound is None:
            self.jump_sound = None
        else:
            self.jump_sound = pygame.mixer.Sound(jump_sound)
            self.jump_sound.set_volume(1.0)

    def play(self, l_events):
        for e in l_events:
            if e.type == KEYDOWN or e.type == KEYUP:
                if e.key == self.key_up:
                    self.key_pressed_up = e.type == KEYDOWN
                elif e.key == self.key_down:
                    self.key_pressed_down = e.type == KEYDOWN
                elif e.key == self.key_left:
                    self.key_pressed_left = e.type == KEYDOWN
                elif e.key == self.key_right:
                    self.key_pressed_right = e.type == KEYDOWN

    def play_auto(self, l_events):
        self.key_pressed_up = False
        self.key_pressed_down = False
        self.key_pressed_left = False
        self.key_pressed_right = False
        for e in l_events:
            if e == "key_pressed_up":
                self.key_pressed_up = True
            elif e == "key_pressed_down":
                self.key_pressed_down = True
            elif e == "key_pressed_left":
                self.key_pressed_left = True
            elif e == "key_pressed_right":
                self.key_pressed_right = True

    def transform(self, flip=False):
        pass

    def update(self, platforms, players):
        min_dist = np.inf
        for p1 in players:
            dist1 = (self.rect.left - p1.rect.left) ** 2 + (self.rect.top - p1.rect.top) ** 2
            if dist1 < min_dist:
                p = p1
                min_dist = dist1

        self.target_player = p

        x_end = int((p.rect.left - self.level_loaded.offset_h) / self.level_loaded.TILE_X)
        y_end = 1+int((p.rect.top - self.level_loaded.offset_w) / self.level_loaded.TILE_Y)
        x_ini = int((self.rect.left - self.level_loaded.offset_h) / self.level_loaded.TILE_X)
        y_ini = 1+int((self.rect.top - self.level_loaded.offset_w) / self.level_loaded.TILE_Y)

        maze = self.level_loaded.level_matrix
        maze_dijkstra = Dijkstra(maze)
        maze_dijkstra.blocked_elements = [-1, 4]

        time_last_calc = (pygame.time.get_ticks() - self.path_last_calc) / 1000
        if self.path is None or time_last_calc > 0.8:
            self.path = maze_dijkstra.shortest_path((y_ini, x_ini), (y_end, x_end))
            self.path_last_calc = pygame.time.get_ticks()

        if len(self.path) > 1:
            if self.path[1].y < self.path[0].y:
                up = True
                down = False
            elif self.path[0].y < self.path[1].y:
                up = False
                down = True
            else:
                if p.rect.top < self.rect.top:
                    up = True
                    down = False
                elif p.rect.top < self.rect.top:
                    up = False
                    down = True
                else:
                    up = False
                    down = False

            if self.path[0].x < self.path[1].x:
                right = True
                left = False
            elif self.path[1].x < self.path[0].x:
                right = False
                left = True
            else:
                if self.rect.left < p.rect.left:
                    right = True
                    left = False
                elif p.rect.left < self.rect.left:
                    right = False
                    left = True
                else:
                    right = False
                    left = False
        else:
            if p.rect.top < self.rect.top:
                up = True
                down = False
            elif p.rect.top < self.rect.top:
                up = False
                down = True
            else:
                up = False
                down = False
            if self.rect.left < p.rect.left:
                right = True
                left = False
            elif p.rect.left < self.rect.left:
                right = False
                left = True
            else:
                right = False
                left = False

        # print("---------------------------------")
        # for c in path:
        #     print(str(c))
        # print("---------------------------------")

        if self.onStairs:
            self.vel_y = 0
            if up: self.vel_y = -self.level_loaded.ENEMY_VELOCITY_MOVEMENT
            if down: self.vel_y = self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        if self.onBar and down:
            self.vel_y = self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        if self.onGround and up:
            # only jump if on the ground
            self.jump_sound.play()
            self.vel_y -= self.level_loaded.VELOCITY_JUMP

        if self.transformed and up and self.vel_y > -self.level_loaded.VELOCITY_FLY_MAX:
            self.vel_y -= self.level_loaded.VELOCITY_FLY
        if self.transformed and down and self.vel_y < self.level_loaded.VELOCITY_FLY_MAX:
            self.vel_y += self.level_loaded.VELOCITY_FLY

        if not self.onGround and not self.onStairs and not self.onBar:
            # only accelerate with gravity if in the air
            self.vel_y += self.level_loaded.GRAVITY
            # max falling speed
            if self.vel_y > self.level_loaded.VELOCITY_FALL_MAX:
                self.vel_y = self.level_loaded.VELOCITY_FALL_MAX

        if left:
            self.vel_x = -self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        if right:
            self.vel_x = self.level_loaded.ENEMY_VELOCITY_MOVEMENT
        if not(left or right):
            self.vel_x = 0
        if not(up or down) and self.onStairs and self.onBar:
            self.vel_y = 0

        # increment in x direction
        self.rect.left += self.vel_x
        # do x-axis collisions
        self.collide(self.vel_x, 0, up, down, left, right, platforms)
        # increment in y direction
        self.rect.top += self.vel_y
        # do y-axis collisions
        self.collide(0, self.vel_y, up, down, left, right, platforms)

    def collide(self, vel_x, vel_y, up, down, left, right, platforms):

        any_stairs = False
        any_bar = False
        self.onGround = False

        for p in platforms:

            if pygame.sprite.collide_rect(self, p) and p is not self:

                if vel_y > 0 and (
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

                if vel_x > 0 and p.collides:
                    self.rect.right = p.rect.left
                    self.vel_x = 0
                if vel_x < 0 and p.collides:
                    self.rect.left = p.rect.right
                    self.vel_x = 0

                if vel_y > 0 and p.collides:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                if vel_y < 0 and p.collides:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0
                if vel_y > 0 and p.has_grip and not (self.onStairs or self.onBar) and not down:
                    # this is like a collision since we are not moving
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0

        if not any_bar and self.onBar and vel_y < 0:
            self.vel_y = 1

        self.onStairs = any_stairs
        self.onBar = any_bar
