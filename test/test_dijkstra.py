from levels import GameLevel
from levels.game_level import load_level, GoalBlockLeft, GoalBlockRight
from levels.level_loaders import GenericWinxLevel
from lib import *


def test_01():
    self = Dijkstra(np.zeros((20, 20)))

    self.maze = np.zeros((20, 20))
    for i in range(4, 15):
        self.maze[10, i] = 1

    x_ini = 1
    y_ini = 10
    x_end = 18
    y_end = 10

    path = self.shortest_path((x_ini, y_ini), (x_end, y_end))

    x_pos = x_end
    y_pos = y_end
    print(str(x_pos) + " : " + str(y_pos))
    while x_ini is not x_pos or y_ini is not y_pos:
        x_pos, y_pos = self.all_paths[x_pos][y_pos]
        print(str(x_pos) + " : " + str(y_pos))


def test_02():
    pygame.mixer.pre_init(48000, -16, 2, 2048)
    pygame.init()
    pygame.display.set_caption("Winx Club")

    # screen_window = pygame.display.set_mode((800, 600))
    screen_window = pygame.display.set_mode((1280, 720))
    # layout = Layout(screen_window, allow_rescale=True)
    layout = Layout(screen_window, allow_rescale=False)

    level_loaded = GenericWinxLevel(layout, "levels/level_txt/level_02.txt", gravity=3)

    layout.screen_desktop.fill(Color("#AAAAAA"))
    layout.screen_game.fill((0, 0, 0))

    (entities, platforms, enemies, players) = load_level(level_loaded)
    player_p1 = players[0]
    if players.__len__() == 1:
        player_p2 = player_p1
    else:
        player_p2 = players[1]

    level_loaded.prepare_background()

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

        if level_loaded.num_players == 1:
            if player_p1.on_goal or player_p2.on_goal:
                done = True
                for p in platforms:
                    if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_full)
            else:
                for p in platforms:
                    if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_empty)

        else:
            if player_p1.on_goal and player_p2.on_goal:
                done = True
                for p in platforms:
                    if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_full)
            elif player_p1.on_goal and not player_p2.on_goal:
                for p in platforms:
                    if isinstance(p, GoalBlockLeft):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_empty)
                    if isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_full)
            elif not player_p1.on_goal and player_p2.on_goal:
                for p in platforms:
                    if isinstance(p, GoalBlockLeft):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_full)
                    if isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_empty)
            else:
                for p in platforms:
                    if isinstance(p, GoalBlockLeft) or isinstance(p, GoalBlockRight):
                        p.set_draw_procedural(level_loaded.TILE_X, level_loaded.TILE_Y, p.image_empty)

        self = enemies[0]
        p = players[0]
        x_end = int((p.rect.top - self.level_loaded.offset_w) / self.level_loaded.TILE_X)
        y_end = int((p.rect.left - self.level_loaded.offset_h) / self.level_loaded.TILE_Y)
        x_ini = int((self.rect.top - self.level_loaded.offset_w) / self.level_loaded.TILE_X)
        y_ini = int((self.rect.left - self.level_loaded.offset_h) / self.level_loaded.TILE_Y)

        level_loaded.print_background()
        entities.draw(layout.screen_game)
        # self.layout.update(player_p2.rect, zoom=2.0)
        layout.update()
        clock.tick(30)

    print("Level finished")


if __name__ == "__main__":
    # test_01()
    test_02()

