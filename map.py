import pygame as pg
from settings import *

#stałe przypisane do zasobów
BUSH_1 = 0
BUSH_2 = 1
ROCK_1 = 2
ROCK_2 = 3
ROCK_3 = 4
WATER = 5

#textury zasobów
textures = {
    BUSH_1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush1.png"), (TILESIZE, TILESIZE)),
    BUSH_2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/bush2.png"), (TILESIZE, TILESIZE)),
    ROCK_1 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock1.png"), (TILESIZE, TILESIZE)),
    ROCK_2 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock2.png"), (TILESIZE, TILESIZE)),
    ROCK_3 : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/rock3.png"), (TILESIZE, TILESIZE)),
    WATER  : pg.transform.scale(pg.image.load(IMAGE_FOLDER + "/water.png"), (TILESIZE, TILESIZE)),
}

#generowanie testowej mapy
test_map = []
for x in range(GRIDWIDTH):
    test_map.append([x % len(textures) for x in range(GRIDHEIGHT)])

#klasa Map odpowiada za wszystko co związane z rysowaniem mapy
class Map:
    def __init__(self, game, path_to_file = ""):
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        if path_to_file == "":
            self.all_fields = test_map
        else:
            load_from_file(path_to_file)

    #rysowanie pomocniczej siatki
    def draw_grid(self, screen):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

    #rysowania całej mapy
    def draw_map(self, screen):
        for row in range(self.width):
            for column in range(self.height):
                screen.blit(textures[self.all_fields[row][column]], (row*TILESIZE, column*TILESIZE))

    def apply_fog(self, screen, player):
        pass

    #wczytywanie mapy z pliku
    def load_from_file(path):
        temp_map_data = []


    def update(self):
        pass
