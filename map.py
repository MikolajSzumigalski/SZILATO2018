import pygame as pg
from settings import *
import copy

#stałe przypisane do zasobów
BUSH_1 = '0'
BUSH_2 = '1'
ROCK_1 = '2'
ROCK_2 = '3'
ROCK_3 = '4'
WATER = '5'
MUD = '6'

#textury zasobów
textures = {
    str(BUSH_1) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush1.png"), (TILESIZE, TILESIZE)),
    str(BUSH_2) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush2.png"), (TILESIZE, TILESIZE)),
    str(ROCK_1) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock1.png"), (TILESIZE, TILESIZE)),
    str(ROCK_2) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock2.png"), (TILESIZE, TILESIZE)),
    str(ROCK_3) : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock3.png"), (TILESIZE, TILESIZE)),
    str(WATER)  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/water.png"), (TILESIZE, TILESIZE)),
    str(MUD)  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/mud.png"), (TILESIZE, TILESIZE)),
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
        for row in range(self.width):
            for column in range(self.height):
                temp_key = self.map_data[column][row]#Te ify, żeby kompilowało się :D W razie czego znajdzie się coś lepszego
                if temp_key == '0':
                    self.tiles_data[column][row] = Bush(self.game, column, row, 1)
                if temp_key == '1':
                    self.tiles_data[column][row] = Bush(self.game, column, row, 2)
                if temp_key == '2':
                    self.tiles_data[column][row] = Rock(self.game, column, row, 1)
                if temp_key == '3':
                    self.tiles_data[column][row] = Rock(self.game, column, row, 2)
                if temp_key == '4':
                    self.tiles_data[column][row] = Rock(self.game, column, row, 3)
                if temp_key == '5':
                    self.tiles_data[column][row] = Water(self.game, column, row, 1)
                if temp_key == '6':
                    self.tiles_data[column][row] = Mud(self.game, column, row, 1)


    def apply_fog(self, screen, player):
        pass

    #wczytywanie mapy z pliku
    def load_from_file(self, file_name):
        self.map_data = []
        with open(MAP_FOLDER + "/" + file_name, "rt") as file:
            for line in file:
                self.map_data.append(line.replace("\n","").split(" "))
        self.camerawidth =  (GRIDWIDTH+4) * TILESIZE
        self.cameraheight =  (GRIDHEIGHT * TILESIZE)
        print(len(self.map_data), len(self.map_data[0]))



    def update(self):
        pass

    def legendReturn(self):
        self.legend = copy.deepcopy(self.map_data)
        print(self.map_data)
        for i in range (0, len(self.legend)):
            for j in range (0, len(self.legend[i])):
                if self.legend[i][j] == '2' or self.legend[i][j] == '3' or self.legend[i][j] == '4':
                    self.legend[i][j] = 1
                else:
                    self.legend[i][j] = 0
        return self.legend

class Tile(pg.sprite.Sprite):
    def __init__(self, game, tileX, tileY, texture):
        self.game = game
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = texture
        self.rect = self.image.get_rect()
        self.x = tileX
        self.y = tileY
        self.rect.x = self.y * TILESIZE
        self.rect.y = self.x * TILESIZE
        self.characterOccupyingTile = None

    def setOccupiedBy(character):
        self.characterOccupyingTile = character

    def isOccupied():
        return self.characterOccupyingTile is not None

class Bush(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush1.png"), (TILESIZE, TILESIZE)),
            2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush2.png"), (TILESIZE, TILESIZE)),
        }
        super(Bush, self).__init__(game, tileX, tileY, self.textures[type])

class Water(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/water.png"), (TILESIZE, TILESIZE)),
        }
        super(Water, self).__init__(game, tileX, tileY, self.textures[type])

class Mud(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/mud.png"), (TILESIZE, TILESIZE)),
        }
        super(Mud, self).__init__(game, tileX, tileY, self.textures[type])

class Rock(Tile):
    def __init__(self, game, tileX, tileY, type):
        self.textures = {
            1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock1.png"), (TILESIZE, TILESIZE)),
            2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock2.png"), (TILESIZE, TILESIZE)),
            3 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock3.png"), (TILESIZE, TILESIZE)),
        }
        super(Rock, self).__init__(game, tileX, tileY, self.textures[type])

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.x = -target.rect.x + int(WIDTH / 2)
        self.y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
