import numpy as np
from lib import Coord


class Dijkstra:

    def __init__(self, maze):
        self.maze = maze
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.blocked_elements = [1]
        self.all_paths = []
        for i in range(0, maze.shape[0]):
            self.all_paths.append([])
            for j in range(0, maze.shape[1]):
                self.all_paths[i].append(Coord((i, j)))

    def set_blocked_elements(self, blocked_elements):
        self.blocked_elements = blocked_elements

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def set_neighbours_arrows(self):
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def set_neighbours_all(self):
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [1, 1], [1, -1], [-1, -1], [-1, 1]]

    def shortest_path(self, ini, end, max_distance=np.inf):
        min_dist = np.full(self.maze.shape, np.inf)

        ini = Coord(ini)
        list_to_explore = [ini]
        min_dist[ini.y, ini.x] = 0

        while list_to_explore:
            current_coord = list_to_explore.pop(0)

            for neighbour in self.neighbours:
                next_coord = current_coord + neighbour
                if next_coord.x < 0 \
                        or next_coord.x >= self.maze.shape[1] \
                        or next_coord.y < 0 \
                        or next_coord.y >= self.maze.shape[0]:
                    continue

                if self.maze[next_coord.y, next_coord.x] in self.blocked_elements:
                    continue

                new_dist = min_dist[current_coord.y, current_coord.x] + np.sqrt(neighbour[0]**2+neighbour[1]**2)
                if new_dist > max_distance:
                    continue

                if new_dist < min_dist[next_coord.y, next_coord.x]:
                    min_dist[next_coord.y, next_coord.x] = new_dist
                    self.all_paths[next_coord.y][next_coord.x] = current_coord
                    list_to_explore.append(next_coord)

        path = [Coord(end)]
        if self.all_paths[Coord(end).y][Coord(end).x].x is not Coord(end).x or \
                self.all_paths[Coord(end).y][Coord(end).x].y is not Coord(end).y:
            while ini.x is not path[0].x or ini.y is not path[0].y:
                if self.all_paths[path[0].y][path[0].x] == path[0]:
                    break
                path = [self.all_paths[path[0].y][path[0].x]] + path

        return path


if __name__ == "__main__":
    self = Dijkstra(np.zeros((20, 20)))

    self.maze = np.zeros((20, 20))
    for i in range(4, 15):
        self.maze[10, i] = 1

    x_ini = 1
    y_ini = 10
    x_end = 18
    y_end = 10

    dist = self.shortest_path((x_ini, y_ini), (x_end, y_end))

    x_pos = x_end
    y_pos = y_end
    print(str(x_pos) + " : " + str(y_pos))
    while x_ini is not x_pos or y_ini is not y_pos:
        x_pos, y_pos = self.all_paths[x_pos][y_pos]
        print(str(x_pos) + " : " + str(y_pos))


