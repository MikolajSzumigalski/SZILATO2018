import pygame as pg
from settings import *

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
        self.width = GRIDWIDTH
        self.height = GRIDHEIGHT
        self.map_data = test_map

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
                temp_key = self.map_data[column][row]
                if temp_key in textures:
                    screen.blit(textures[self.map_data[column][row]], (row*TILESIZE, column*TILESIZE))

    def apply_fog(self, screen, player):
        pass

    #wczytywanie mapy z pliku
    def load_from_file(self, file_name):
        self.map_data = []
        with open(MAP_FOLDER + "/" + file_name, "rt") as file:
            for line in file:
                self.map_data.append(line.replace("\n","").split(" "))
        print(len(self.map_data), len(self.map_data[0]))



    def update(self):
        pass
