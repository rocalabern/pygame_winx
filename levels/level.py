import pygame
from lib import *


def read_level(str_file):
    with open(str_file) as f:
        line_list = f.readlines()

    line_list = [line.rstrip('\n') for line in open(str_file)]
    return line_list


def get_background_tile_simple(tile_x, tile_y):
    bg = Surface((tile_x, tile_y))
    bg.convert()

    bg.fill(Color("#ffe6e6"))
    bg.fill(Color("#ffffff"), Rect(2, 2, tile_x-2, tile_y-2))

    return bg

class Level:

    def __init__(
            self,
            layout: Layout,
            level_file: str,
            velocity_movement=4,
            velocity_jump=4,
            velocity_fly=1,
            velocity_fly_max=12,
            num_players: int = 0
    ):
        self.layout = layout
        self.LEVEL_FILE = level_file
        self.level = read_level(self.LEVEL_FILE)
        self.TILE_Y_NUM = self.level.__len__()
        self.TILE_X_NUM = self.level[0].__len__()

        self.VELOCITY_MOVEMENT = velocity_movement
        self.VELOCITY_JUMP = velocity_jump
        self.VELOCITY_MAX_FALL = 10

        self.VELOCITY_FLY = velocity_fly
        self.VELOCITY_FLY_MAX = velocity_fly_max

        self.num_players = num_players

    def prepare_background(self):
        print("[Level] prepare_background")
        self.bg_color = Color("#000000")

    def print_background(self):
        self.layout.screen_game.fill(self.bg_color)

    def success_animation(self):
        print("[Level] success_animation")
