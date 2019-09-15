import sys
import pygame
from pygame import *
from layout.layout import Layout

from levels import Level
from lib import *
from entities import *


def load_level(level_loaded: Level):
    tile_x = level_loaded.TILE_X
    tile_y = level_loaded.TILE_Y
    offset_w = level_loaded.offset_w
    offset_h = level_loaded.offset_h

    entities = pygame.sprite.Group()
    platforms = []
    enemies = []

    # build the level
    player_p1 = Player(level_loaded, 0, 0, "dummy")
    player_p2 = Player(level_loaded, 0, 0, "dummy")
    y = offset_h
    for level_row in level_loaded.level:
        x = offset_w
        for level_block in level_row:
            if level_block == "▉" or level_block == "P":
                e = PlatformBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "╬" or level_block == "E":
                e = StairsBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "-" or level_block == "B":
                e = BarBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "_" or level_block == "H":
                e = BarHBlock(x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "⊟" or level_block == "G":
                e = GoalBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "⊏" or level_block == "L":
                e = GoalBlockLeft(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
            if level_block == "⊐" or level_block == "R":
                e = GoalBlockRight(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)

            if level_block == "⭐" or level_block == "S":
                e = StarItem(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)

            if level_block == "T":
                e = Tritannus(
                    level_loaded,
                    x, y, "Y",
                    constants.PLAYER_P1_COLOR_BG,
                    constants.IMAGE_P1,
                    constants.IMAGE_P1_TRANSFORMED,
                    flip=True,
                    jump_sound=constants.PLAYER_P1_JUMP
                )
                entities.add(e)
                enemies.append(e)

            if level_block == "1" or level_block == "Y":
                player_p1 = Player(
                    level_loaded,
                    x, y, "Y",
                    constants.PLAYER_P1_COLOR_BG,
                    constants.IMAGE_P1,
                    constants.IMAGE_P1_TRANSFORMED,
                    flip=True,
                    jump_sound=constants.PLAYER_P1_JUMP
                )
                level_loaded.num_players = level_loaded.num_players + 1

            if level_block == "2" or level_block == "X":
                player_p2 = Player(
                    level_loaded,
                    x, y, "X",
                    constants.PLAYER_P2_COLOR_BG, constants.IMAGE_P2,
                    constants.IMAGE_P2_TRANSFORMED,
                    flip=True,
                    jump_sound=constants.PLAYER_P2_JUMP
                )
                level_loaded.num_players = level_loaded.num_players + 1

            x += tile_x
        y += tile_y
    if player_p1.name is not "Dummy":
        platforms.append(player_p1)
        entities.add(player_p1)
    if player_p2.name is not "Dummy":
        entities.add(player_p2)
        platforms.append(player_p2)
    return entities, platforms, enemies, player_p1, player_p2


class GameLevel:

    def __init__(self, level_loaded):
        self.level_loaded = level_loaded
        self.layout = level_loaded.layout

    def play(self):
        self.layout.screen_desktop.fill(Color("#AAAAAA"))
        self.layout.screen_game.fill((0, 0, 0))

        (entities, platforms, enemies, player_p1, player_p2) = load_level(self.level_loaded)

        music_file = 'music/instrumental-winx-club-butterflix.mp3'
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.level_loaded.prepare_background()

        up_p1 = down_p1 = left_p1 = right_p1 = False
        up_p2 = down_p2 = left_p2 = right_p2 = False

        clock = pygame.time.Clock()
        done = False
        skip = False
        while not done:

            # e: event
            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit("ESCAPE")
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit("ESCAPE")
                if e.type == KEYDOWN and e.key == K_F2:
                    done = True
                if e.type == KEYDOWN and e.key == K_F3:
                    done = True
                    skip = True

                if e.type == KEYDOWN or e.type == KEYUP:

                    if e.key == K_UP:
                        up_p1 = e.type == KEYDOWN
                    if e.key == K_DOWN:
                        down_p1 = e.type == KEYDOWN
                    if e.key == K_LEFT:
                        left_p1 = e.type == KEYDOWN
                    if e.key == K_RIGHT:
                        right_p1 = e.type == KEYDOWN

                    if e.key == K_w:
                        up_p2 = e.type == KEYDOWN
                    if e.key == K_s:
                        down_p2 = e.type == KEYDOWN
                    if e.key == K_a:
                        left_p2 = e.type == KEYDOWN
                    if e.key == K_d:
                        right_p2 = e.type == KEYDOWN

            # update player, draw everything else
            player_p1.update(up_p1, down_p1, left_p1, right_p1, platforms)
            player_p2.update(up_p2, down_p2, left_p2, right_p2, platforms)
            for e in enemies:
                e.update(platforms, player_p1, player_p2)

            if self.level_loaded.num_players == 1:
                if player_p1.on_goal or player_p2.on_goal:
                    done = True
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_full)
                else:
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_empty)

            else:
                if player_p1.on_goal and player_p2.on_goal:
                    done = True
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_full)
                elif player_p1.on_goal and not player_p2.on_goal:
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_empty)
                        if isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_full)
                elif not player_p1.on_goal and player_p2.on_goal:
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_full)
                        if isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_empty)
                else:
                    for p in platforms:
                        if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                            p.set_draw_procedural(self.level_loaded.TILE_X, self.level_loaded.TILE_Y, p.image_empty)

            self.level_loaded.print_background()
            entities.draw(self.layout.screen_game)
            # self.layout.update(player_p2.rect, zoom=1.2)
            self.layout.update()
            clock.tick(60)

        print("Level finished")
        if not skip:
            print("Level finished : not skipped")
            pygame.time.wait(1000)
            if self.level_loaded.success_animation is not None:
                print("Level finished : Doing final animation")
                self.level_loaded.success_animation()

                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN and (event.key == K_F2 or event.key == K_F3 or event.key == K_F10):
                            return
                    clock.tick(60)
