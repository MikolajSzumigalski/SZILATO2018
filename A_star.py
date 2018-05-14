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

class A_star_path:
    def __init__(self, LogicEngine):
        self.start = [LogicEngine.player.x, LogicEngine.player.y]
        self.monsters = LogicEngine.get_monsters_positions()
        self.mixtures = LogicEngine.get_mixtures_positions()
        self.map = LogicEngine.map
        self.spot_map = [[0 for j in range(self.map.width)] for i in range(self.map.height)]

        #TO DO: naprawić błąd ze złymi współrzędnymi mapy!!!
        for x in range(self.map.width):
            for y in range(self.map.height):
                self.spot_map[y][x] = Spot(x, y, LogicEngine.map.tiles_data[y][x].isCollidable or [x, y] in self.monsters + self.mixtures, 1)
        # self.log_map()

    def log_map(self):
        #debug
            for y in range(0, self.map.height):
                for x in range(0, self.map.width):
                    if self.spot_map[y][x].is_wall:
                        print ("#", end='')
                    else:
                        print(".", end='')
                print("")

    def get_spot(self, pos):
        return self.spot_map[pos[1]][pos[0]]

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

    def get_available_neighbours(self, spot):
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
        self.get_spot(dest).is_wall = False

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

            for n in self.get_available_neighbours(current):

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


class A_star_target_list:
    def __init__(self, LogicEngine):
        self.game = LogicEngine

    def get_new_plan(self):
        return self.game.monsters + self.game.mixtures

