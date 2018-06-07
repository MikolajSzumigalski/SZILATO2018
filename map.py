import pygame as pg
from settings import *
from sprites import *
import copy
import random

#stałe przypisane do zasobów
BUSH_1 = '0'
BUSH_2 = '1'
ROCK_1 = '2'
ROCK_2 = '3'
ROCK_3 = '4'
WATER = '5'

#textury zasobów
textures = {
    str(BUSH_1) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush1.png"), (TILESIZE, TILESIZE)),
    str(BUSH_2) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush2.png"), (TILESIZE, TILESIZE)),
    str(ROCK_1) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock1.png"), (TILESIZE, TILESIZE)),
    str(ROCK_2) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock2.png"), (TILESIZE, TILESIZE)),
    str(ROCK_3) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock3.png"), (TILESIZE, TILESIZE)),
    str(WATER)  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/water.png"), (TILESIZE, TILESIZE)),
}

#generowanie testowej mapy
test_map = []
for x in range(GRIDWIDTH):
    test_map.append([str(x % len(textures)) for x in range(GRIDHEIGHT)])


#klasa Map odpowiada za wszystko co związane z rysowaniem mapy
class Map:
    def __init__(self, game):
        self.game = game
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.camerawidth =  0
        self.cameraheight = 0
        self.map_data = test_map
        self.tiles_data = [[0 for j in range(self.width)] for i in range(self.height)]
        print("debug", len(self.tiles_data), len(self.tiles_data[0]))

    #rysowanie pomocniczej siatki
    def draw_grid(self, screen):
        for x in range(0, MAP_WIDTH, TILESIZE):
            pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

    #rysowania całej mapy
    #def draw_map(self, screen):
    #    for row in range(self.width):
    #        for column in range(self.height):
    #            temp_key = self.map_data[column][row]
    #            if temp_key in textures:
    #                screen.blit(self.tiles_data[column][row].image, (row*TILESIZE, column*TILESIZE))


    def init_tile_objects(self):
        for row in range(self.height):
            for column in range(self.width):
                temp_key = self.map_data[row][column]#Te ify, żeby kompilowało się :D W razie czego znajdzie się coś lepszego
                # print(temp_key, end='')
                if temp_key == '0':
                    self.tiles_data[row][column] = Bush(self.game, column, row, 1)
                if temp_key == '1':
                    self.tiles_data[row][column] = Bush(self.game, column, row, 2)
                if temp_key == '2':
                    self.tiles_data[row][column] = Rock(self.game, column, row, 1)
                if temp_key == '3':
                    self.tiles_data[row][column] = Rock(self.game, column, row, 2)
                if temp_key == '4':
                    self.tiles_data[row][column] = Rock(self.game, column, row, 3)
                if temp_key == '5':
                    self.tiles_data[row][column] = Water(self.game, column, row, 1)
                if temp_key == '.':
                    self.tiles_data[row][column] = Grass(self.game, column, row, 1)


    def apply_fog(self, screen, player):
        pass

    #wczytywanie mapy z pliku
    def load_from_file(self, file_name="test_map", random_objects=True):
        self.map_data = []
        temp_arr = []
        with open(MAP_FOLDER + "/" + file_name, "rt") as file:
            state = 0 # 0 - wymiary,
            temp_count = 0 # ilość potworów do wygenerowania
            for line in file:
                if state == 0:
                    size = line.replace("\n","").split(";")
                    GRIDWIDTH = int(size[0])
                    GRIDHEIGHT = int(size[1])
                    state = 1
                    continue
                if state == 1:
                    if line[0] == "#":
                        if random_objects: break
                        state = 2
                        continue
                    self.map_data.append(line.replace("\n","").split(" "))
                if state == 2:
                    if line[0] == "#": break
                    temp_arr.append(list(map(int, line.replace("\n","").split(";"))))

        self.camerawidth =  (GRIDWIDTH+4) * TILESIZE
        self.cameraheight =  (GRIDHEIGHT * TILESIZE)
        self.init_tile_objects()
        if random_objects:
            self.random_spawn_monsters()
            self.random_spawn_intems()
        else:
            for line_arr in temp_arr:
                    if   line_arr[0] == 0:
                        obj = Mglak(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 1:
                        obj = Spider(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 2:
                        obj = Ghoul(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 3:
                        obj = Leszy(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)                        
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 4:
                        obj = Olgierd(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 5:
                        obj = Dragon(self.game, line_arr[1], line_arr[2])
                        self.game.monsters.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
                    elif line_arr[0] == 6:
                        obj = HP_Mixture(self.game, line_arr[1], line_arr[2])
                        self.game.mixtures.append(obj)
                        getTileData(obj.x, obj.y).setOccupiedBy(obj)
    def update(self):
        pass

    def getTileData(x,y):
        return self.tiles_data[y][x]
    def legendReturn(self):
        self.legend = copy.deepcopy(self.map_data)
        for i in range (0, len(self.legend)):
            for j in range (0, len(self.legend[i])):
                if self.legend[i][j] == '2' or self.legend[i][j] == '3' or self.legend[i][j] == '4' or self.legend[i][j] == '5':
                    self.legend[i][j] = 1
                else:
                    self.legend[i][j] = 0
        return self.legend

    def random_spawn_monsters(self):
        for i in range (0, 10):
            rand = random.randint(0, len(MAP_PLACES)-1)
            obj = Mglak(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1])
            self.game.monsters.append(obj)
            getTileData(obj.x, obj.y).setOccupiedBy(obj)
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 8):
            rand = random.randint(0, len(MAP_PLACES)-1)
            obj = Spider(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1])
            self.game.monsters.append(obj)
            getTileData(obj.x, obj.y).setOccupiedBy(obj)
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 8):
            rand = random.randint(0, len(MAP_PLACES)-1)
            obj = Ghoul(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1])
            self.game.monsters.append(obj)
            getTileData(obj.x, obj.y).setOccupiedBy(obj)
            MAP_PLACES.remove(MAP_PLACES[rand])
        #
        for i in range (0, 1):
            rand = random.randint(0, len(MAP_PLACES)-1)
            obj = Leszy(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1])
            self.game.monsters.append(obj)
            getTileData(obj.x, obj.y).setOccupiedBy(obj)
            MAP_PLACES.remove(MAP_PLACES[rand])

        # for i in range (0, 1):
        #     rand = random.randint(0, len(MAP_PLACES)-1)
        #     self.game.monsters.append(Olgierd(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
        #     MAP_PLACES.remove(MAP_PLACES[rand])

        # for i in range (0, 1):
        #     rand = random.randint(0, len(MAP_PLACES)-1)
        #     self.game.monsters.append(Dragon(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
        #     MAP_PLACES.remove(MAP_PLACES[rand])

    def random_spawn_intems(self):
        for i in range (0, 3):
            rand = random.randint(0, len(MAP_PLACES))
            obj = HP_Mixture(self.game, MAP_PLACES[rand][0], MAP_PLACES[rand][1])
            self.game.mixtures.append(obj)
            getTileData(obj.x, obj.y).setOccupiedBy(obj)
            MAP_PLACES.remove(MAP_PLACES[rand])

class Tile(pg.sprite.Sprite):
    def __init__(self, game, tileX, tileY, texture):
        self.logic_attribute_name_list = ['x', 'y', 'name', 'id', 'isCollidable', 'logic_attribute_name_list','characterOccupyingTile'];
        self.game = game
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = texture
        self.rect = self.image.get_rect()
        #ATRYBUTY LOGICZNE
        self.x = tileX
        self.y = tileY
        self.name = self.__class__.__name__
        self.id = id(self)
        self.isCollidable = None;

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.characterOccupyingTile = None

        # # zmienne potrzebne do A*
        # self.h = 0
        # self.g = 0
        # self.f = 0

    # Te rzeczy są po to, by branie klasy i próbowanie jej wyprintowania etc. dawało tylko i wyłącznie
    # rzeczy logicznie, x, y, nazwa
    def __getstate__(self):
        state = self.__dict__.copy()
        try:
            newstate = {k: state[k] for k in self.logic_attribute_name_list}
        except AttributeError:
            newstate = {k: state[k] for k in ['x', 'y', 'name', 'id', 'isCollidable', 'logic_attribute_name_list']}
        return newstate

    def __setstate__(self, state):
        self.__dict__.update(state)

    def setOccupiedBy(self, character):
        self.characterOccupyingTile = character

    def isOccupied(self):
        return self.characterOccupyingTile is not None

#gdy dodejemy nowy typ pola trzeba pamiętać by dodać pole isCollidable (True | False),
#oraz moveCost gdy isCollidable jest False

class Grass(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/grass.png"), (TILESIZE, TILESIZE)),
        }
        super().__init__(game, tileX, tileY, self.textures[type])
        self.isCollidable = False
        self.moveCost = 1

class Bush(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush1.png"), (TILESIZE, TILESIZE)),
            2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush2.png"), (TILESIZE, TILESIZE)),
        }
        super().__init__(game, tileX, tileY, self.textures[type])
        self.isCollidable = False
        self.moveCost = 5

class Water(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/water.png"), (TILESIZE, TILESIZE)),
        }
        super().__init__(game, tileX, tileY, self.textures[type])
        self.isCollidable = True

class Rock(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock1.png"), (TILESIZE, TILESIZE)),
            2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock2.png"), (TILESIZE, TILESIZE)),
            3 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock3.png"), (TILESIZE, TILESIZE)),
        }
        super().__init__(game, tileX, tileY, self.textures[type])
        self.isCollidable = True

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.window_x + int(WIDTH / 2)
        y = -target.window_y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
