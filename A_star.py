from map import *
from game import *

class Spot:
    def __init__(self, x, y, is_wall, cost=10000):
        self.is_wall = is_wall
        self.cost = cost
        self.x = x
        self.y = y
        self.g = 10000
        self.f = 0

    def get_pos(self):
        return [self.x, self.y]

class A_star:
    def __init__(self, game):
        self.start = [game.player.x, game.player.y]
        self.monsters = game.get_monsters_positions()
        self.mixtures = game.get_mixtures_positions()
        self.map = game.map
        self.spot_map = [[0 for j in range(self.map.width)] for i in range(self.map.height)]

        #TO DO: naprawić błąd ze złymi współrzędnymi mapy!!!
        for i in range(0, self.map.width):
            for j in range(0, self.map.height):
                self.spot_map[i][j] = Spot(i, j, game.map.tiles_data[j][i].isCollidable or [i,j] in self.monsters, 1)
        self.log_map()

    def log_map(self):
        #debug
            for j in range(0, self.map.height):
                for i in range(0, self.map.width):
                    if self.spot_map[i][j].is_wall:
                        print ("#", end='')
                    else:
                        print(".", end='')
                print("")

    def get_spot(self, pos):
        return self.spot_map[pos[0]][pos[1]]

    def manhattan_dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def lowest_f_cost_spot(self, openList):
        min_cost_spot = openList[0]
        for i in range(0, len(openList)):
            if openList[i].f < min_cost_spot.f:
                min_cost_spot = openList[i]
        return min_cost_spot

    def reconstruct_path(self, cameFrom, current):
        path = [current.get_pos()]
        while  current in cameFrom:
            current = cameFrom[current]
            path.insert(0, current.get_pos())

        return path

    def get_avalible_neighbours(self, spot):
        #pozyskaj sąsiadów któży nie są ścianą lub potworem
        out = []
        x = spot.x
        y = spot.y
        # north neighbour
        if spot.y - 1 >= 0:
            if not self.get_spot([x, y-1]).is_wall:
                out.append(self.get_spot([x, y-1]))
        # south neighbour
        if spot.y + 1 < self.map.height:
            if not self.get_spot([x, y+1]).is_wall:
                out.append(self.get_spot([x, y+1]))
        # west neighbour
        if spot.x - 1 >= 0:
            if not self.get_spot([x-1, y]).is_wall:
                out.append(self.get_spot([x-1, y]))
        # east neighbour
        if spot.x + 1 < self.map.width:
            if not self.get_spot([x+1, y]).is_wall:
                out.append(self.get_spot([x+1, y]))
        return out

    def get_path_to(self, dest):
        start_spot = self.get_spot(self.start)
        openSet = [start_spot]
        closedSet = []
        cameFrom = {}

        start_spot.g = 0
        start_spot.f = self.manhattan_dist(self.start, dest)

        while openSet:
            current = self.lowest_f_cost_spot(openSet)
            # print([current.x, current.y])
            if [current.x, current.y] == dest:
                print ("Path exists!")
                return self.reconstruct_path(cameFrom, current)

            openSet.remove(current)
            closedSet.append(current)

            for n in self.get_avalible_neighbours(current):

                if n in closedSet:
                    continue
                if not n in openSet:
                    openSet.append(n)
                temp_g_score = current.g + n.cost
                if temp_g_score >= n.g:
                    continue
                cameFrom[n] = current
                n.g = temp_g_score
                n.f = n.g + self.manhattan_dist([n.x, n.y], dest)

        print("There is no path!")
        return []
