from game import *
import copy
import random

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
    def __init__(self, game, exceptions=[]):
        self.exceptions = list(exceptions)
        self.start = [game.player.x, game.player.y]
        self.monsters = game.get_monsters_positions()
        self.items = game.get_items_positions()
        self.map = game.map
        self.spot_map = [[0 for j in range(self.map.width)] for i in range(self.map.height)]

        for m in game.monsters:
            if not m.alive: self.exceptions.append([m.x, m.y])
        for i in game.items:
            if not i.alive: self.exceptions.append([i.x, i.y])

        for x in range(self.map.width):
            for y in range(self.map.height):
                self.spot_map[y][x] = Spot(x, y, [x,y] not in self.exceptions and (game.map.tiles_data[y][x].isCollidable or [x,y] in self.monsters + self.items), 1)
        # print(self.spot_map[3][7].is_wall)

    def set_start(self, pos):
        self.start = pos

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

    def get_path_to(self, dest, only_lenght=False):
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
                # print ("Path exists!")
                if only_lenght:
                    return len(self.reconstruct_path(cameFrom, current))
                else:
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

        # print("There is no path!")
        if not only_lenght:
            return []
        else:
            return -1


class State:
    #klasa obiektu przechowującego wszystkie informacje o stanie, oraz wszystkie metody pomocnicze
    def __init__(self, player, monsters, items, engine, action, parent):
        self.player = player
        self.monsters = monsters
        self.items = items
        self.engine = engine
        self.action = action
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = self.get_f_score()


    def __eq__(self, other):
        p1 = self.player
        p2 = other.player
        if p1.hp != p2.hp or p1.lev != p2.lev or p1.at != p2.at or p1.deff != p2.deff:
            return False
        for m1,m2 in zip(self.monsters, other.monsters):
            if m1.hp != m2.hp:
                return False
        for i1,i2 in zip(self.items, other.items):
            if i1.alive != i2.alive:
                return False
        return True

    def get_state_as_array(self):
        return [self.player] + self.monsters + self.items

    def all_unactive_objects(self):
        out = []
        for m in self.monsters:
            if not m.alive: out.append([m.x, m.y])
        for i in self.items:
            if not i.alive: out.append([i.x, i.y])
        return out

    def alive_monsters_count(self):
        out = 0
        for m in self.monsters:
            if m.alive: out += 1
        return out

    def get_all_hp(self):
        out = 0
        for m in self.monsters:
            out += m.hp
        return out

    def random_monster(self):
        return random.choice(self.monsters)

    def get_f_score(self):
        return self.g + self.h



class A_star_target_list:

    def __init__(self, game):
        self.game = game
        #początkowy stan ma pola parent i action ustawione na None, przydatne w self.get_instructions_chain()
        self.start_state = State(game.player, game.monsters, game.items, game.logic_engine, None, None)

    def next_state(self, object_to_visit, state):
        #przy pomocy symulwanego silnika logicznego z game_logic.py pozyskujemy kolejny stan
        new_engine = state.engine.simulate_move_absolute_coordinate(False, object_to_visit.x, object_to_visit.y)
        return State(new_engine.player, new_engine.monsters, new_engine.items, new_engine, object_to_visit, state)

    def get_all_lenghts(self, state):
        #pozyskaj tablicę odległości do poszczególnych obiektów Monster|Item ze stanu 'state'
        temp_arr = state.get_state_as_array()[1:]
        out = []
        for obj in temp_arr:
            #jeśli obiekt nie jest aktywny, nie bierzemy go pod uwagę
            if not obj.alive:
                out.append(-1)
                continue
            A = A_star_path(self.game, state.all_unactive_objects())
            A.set_start([state.player.x, state.player.y])
            out.append(A.get_path_to([obj.x, obj.y], True))
        return out

    def get_min_f_score_state(self, state_array):
        #z listy 'state_array' wybierz stan z najmniejszym f-score (state.f), usuń go z listy
        min_state = state_array[0]
        for i in range(1, len(state_array)):
            if state_array[i].f < min_state.f:
                min_state = state_array[i]
        state_array.remove(min_state)
        return min_state

    def get_instructions_chain(self, state):
        #rekonstrukcja ciągu akcji od obecnego stanu do początku, gdzie state.akcja = None
        out = []
        temp_state = state
        while not temp_state.action == None:
            out.insert(0,temp_state.action)
            temp_state = temp_state.parent
        return out

    def get_new_plan(self):
        #wygeneruj listę akcji (obiektów) które bohater musi wykonać (odwiedzić) by zlikwidować wszystkie
        #potwory w optymalnej liczbie kroków

        print("Start A*")

        open_list = [self.start_state]
        closed_list = []

        while open_list:
            #wybranie stanu z najmniejszym kosztem f = g + h ,z listy kandydatów
            current_state = self.get_min_f_score_state(open_list)

            #jeśli dotarliśmy do celu
            if current_state.get_all_hp() <= 0 and current_state.player.hp > 0:
                print("znaleziono!")
                #generowanie łańcucha akcji
                return self.get_instructions_chain(current_state)

            closed_list.append(current_state)
            current_lengths = self.get_all_lenghts(current_state)

            for o,l in zip(current_state.get_state_as_array()[1:], current_lengths):
                #o - obiekt typu Monster|Item
                #l - odległość z aktualnej pozycji do tego obiektu (A*)

                #jeśli nie można dojść to tego obiektu
                if l == -1:
                    continue
                #nowy stan new_state
                new_state = self.next_state(o, current_state)

                #koszt dotarcia
                new_state.g = current_state.g + l
                #heurystyka
                new_state.h = new_state.get_all_hp() + new_state.alive_monsters_count() * 100 - new_state.player.hp
                new_state.f = new_state.g*2 + new_state.h
                # print(new_state.f, " ", end='')

                '''
                mamy teraz 3 możliwości:
                1) 'new_state' jest już w open_list[] - jeśli znaleziony stan.f > new_state.f, zastępujemy stan -> new_state
                2) 'new_state' jest już w closed_list[] - ignorujemy 'new_state'
                3) 'new_stet' nie ma ani w open_list[], anie w closed_list[] - wrzucamy 'new_state' do open_list[]
                '''

                in_open_list = False
                in_closed_list = False
                for s in open_list:
                    if s == new_state:
                        if s.f > new_state.f:
                            s.parent = new_state.parent
                            s.engine = new_state.engine
                            s.action = new_state.action
                            s.f = new_state.f
                            s.g = new_state.g
                            in_open_list = True
                            break
                if in_open_list:
                    continue
                for s in closed_list:
                    if s == new_state:
                        in_closed_list = True
                        break
                if not in_closed_list:
                    open_list.append(new_state)

            # print("")

        print("nie znaleziono!")
        return []
