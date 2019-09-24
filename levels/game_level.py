import sys
import pygame
from pygame import *

from entities.enemy import Enemy
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
    players = []

    # build the level
    y = offset_h
    for i_row in range(0, level_loaded.TILE_Y_NUM):
        x = offset_w
        level_row = level_loaded.level[i_row]
        for i_col in range(0, level_loaded.TILE_X_NUM):
            level_block = level_row[i_col]
            level_loaded.level_matrix[i_row][i_col] = 0
            if level_block == "▉" or level_block == "P":
                e = PlatformBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = -1
            if level_block == "╬" or level_block == "E":
                e = StairsBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = 2
            if level_block == "-" or level_block == "B":
                e = BarBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = 3
            if level_block == "_" or level_block == "H":
                e = BarHBlock(x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = 3
            if level_block == "⊟" or level_block == "G":
                e = GoalBlock(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = -1
            if level_block == "⊏" or level_block == "L":
                e = GoalBlockLeft(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = -1
            if level_block == "⊐" or level_block == "R":
                e = GoalBlockRight(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)
                level_loaded.level_matrix[i_row][i_col] = -1

            if level_block == "⭐" or level_block == "S":
                e = StarItem(level_loaded, x, y)
                platforms.append(e)
                entities.add(e)

            if level_block == "g":
                e = Ghost(
                    level_loaded,
                    x, y, "Ghost",
                    bg_color="#72A877",
                    image_file='images/sprites/characters/enemies/ghost.png',
                    flip=True,
                    jump_sound=constants.PLAYER_P1_JUMP
                )
                entities.add(e)
                enemies.append(e)
            if level_block == "t":
                e = Enemy(
                    level_loaded,
                    x, y, "Tritannus",
                    None, None, None, None,
                    bg_color="#72A877",
                    image_file='images/winx_raw/tritannus_01.png',
                    flip=True,
                    jump_sound=constants.PLAYER_P1_JUMP
                )
                entities.add(e)
                enemies.append(e)

            if level_block == "1" or level_block == "Y":
                e = Player(
                    level_loaded,
                    x, y, "Y",
                    K_UP, K_DOWN, K_RIGHT, K_LEFT,
                    constants.PLAYER_P1_COLOR_BG,
                    constants.IMAGE_P1,
                    constants.IMAGE_P1_TRANSFORMED,
                    flip=True,
                    jump_sound=constants.PLAYER_P1_JUMP
                )
                level_loaded.num_players = level_loaded.num_players + 1
                players.append(e)
                player_p1 = e

            if level_block == "2" or level_block == "X":
                e = Player(
                    level_loaded,
                    x, y, "X",
                    K_w, K_s, K_d, K_a,
                    constants.PLAYER_P2_COLOR_BG, constants.IMAGE_P2,
                    constants.IMAGE_P2_TRANSFORMED,
                    flip=True,
                    jump_sound=constants.PLAYER_P2_JUMP
                )
                level_loaded.num_players = level_loaded.num_players + 1
                players.append(e)
                player_p2 = e

            x += tile_x
        y += tile_y

    for i_row in range(0, level_loaded.TILE_Y_NUM-1):
        for i_col in range(0, level_loaded.TILE_X_NUM):
            if i_row < level_loaded.TILE_Y_NUM-1:
                if level_loaded.level_matrix[i_row+1][i_col] == -1:
                    level_loaded.level_matrix[i_row][i_col] = 1
                if level_loaded.level_matrix[i_row + 1][i_col] == 2:
                    level_loaded.level_matrix[i_row][i_col] = 1
                if level_loaded.level_matrix[i_row + 1][i_col] == 3:
                    level_loaded.level_matrix[i_row][i_col] = 3

    for p in players:
        entities.add(p)
        platforms.append(p)
    return entities, platforms, enemies, players


class GameLevel:

    def __init__(self, level_loaded):
        self.level_loaded = level_loaded
        self.layout = level_loaded.layout

    def play(self):
        self.layout.screen_desktop.fill(Color("#AAAAAA"))
        self.layout.screen_game.fill((0, 0, 0))

        (entities, platforms, enemies, players) = load_level(self.level_loaded)
        player_p1 = players[0]
        if players.__len__() == 1:
            player_p2 = player_p1
        else:
            player_p2 = players[1]

        # music_file = 'music/instrumental-winx-club-butterflix.mp3'
        # pygame.mixer.music.load(music_file)
        # pygame.mixer.music.set_volume(0.1)
        # pygame.mixer.music.play(-1)

        self.level_loaded.prepare_background()

        clock = pygame.time.Clock()
        done = False
        skip = False
        while not done:

            # e: event
            l_events = pygame.event.get()
            for e in l_events:
                if e.type == QUIT:
                    raise SystemExit("ESCAPE")
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit("ESCAPE")
                if e.type == KEYDOWN and e.key == K_F2:
                    done = True
                if e.type == KEYDOWN and e.key == K_F3:
                    done = True
                    skip = True

            for player in players:
                player.play(l_events)
                player.update(platforms)

            for e in enemies:
                e.update(platforms, players)

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
            # self.layout.update(player_p2.rect, zoom=2.0)
            self.layout.update()
            clock.tick(30)

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
