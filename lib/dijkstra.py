import numpy as np
from lib import Coord


class Dijkstra:

    def __init__(self, maze):
        self.maze = maze
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        self.path = []
        for i in range(0, maze.shape[0]):
            self.path.append([])
            for j in range(0, maze.shape[1]):
                self.path[i].append((i, j))

    def set_neighbours_arrows(self):
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def set_neighbours_all(self):
        self.neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [1, 1], [1, -1], [-1, -1], [-1, 1]]

    def shortest_path(self, ini, end, max_distance=np.inf):
        ini = Coord(ini)
        end = Coord(end)

        dist = np.full(self.maze.shape, np.inf)

        # we start here, thus a distance of 0
        open_list = [ini]
        dist[ini.x, ini.y] = 0

        # (x,y) offsets from current cell
        while open_list:
            current_coord = open_list.pop(0)

            for neighbour in self.neighbours:
                next_coord = current_coord + neighbour
                if next_coord.x < 0 \
                        or next_coord.x >= self.maze.shape[0] \
                        or next_coord.y < 0 \
                        or next_coord.y >= self.maze.shape[1]:
                    continue

                if self.maze[next_coord.x, next_coord.y] == 1:
                    continue

                new_dist = dist[current_coord.x, current_coord.y] + np.sqrt(neighbour[0]**2+neighbour[1]**2)
                if new_dist > max_distance:
                    continue

                if new_dist < dist[next_coord.x, next_coord.y]:
                    dist[next_coord.x, next_coord.y] = new_dist
                    self.path[next_coord.x][next_coord.y] = current_coord
                    open_list.append(next_coord)

        return dist


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

    dist[10,]

    x_pos = x_end
    y_pos = y_end
    print(str(x_pos) + " : " + str(y_pos))
    while x_ini is not x_pos or y_ini is not y_pos:
        x_pos, y_pos = self.path[x_pos][y_pos]
        print(str(x_pos) + " : " + str(y_pos))


