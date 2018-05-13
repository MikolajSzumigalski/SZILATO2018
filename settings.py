import os

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (60, 60, 60)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 55, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)

# game settings
WIDTH = 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 500  # 16 * 48 or 32 * 24 or 64 * 12
MAP_WIDTH = 600
FPS = 60
TITLE = "Sztuczny Wiedźmin i przyjaciele"
BGCOLOR = DARKGREY

# default settings
TILESIZE = 50

GAME_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_FOLDER, "img")
MAP_FOLDER = os.path.join(GAME_FOLDER, "maps")

# MAP = "labirynt_szumi_deluxe.map"
MAP = "labirynt_szumi_deluxe.map"
MAPLIST = []
MAP_PLACES = []

#TO DO: przenieść do mapy!!!
with open(MAP_FOLDER + "/" + MAP, "rt") as file:
    state = 0
    for line in file:
        if state == 0:
            state = 1
            continue
        if state == 1:
            if line[0] == "#": break
            MAPLIST.append(line.replace("\n","").split(" "))

GRIDWIDTH = len(MAPLIST[0])
GRIDHEIGHT = len(MAPLIST)
print("[debug] ",GRIDWIDTH, GRIDHEIGHT)
RANDOM_SPAWN = True

for i in range (0, GRIDHEIGHT):
    for j in range (0, GRIDWIDTH):
        if MAPLIST[i][j] == ".":
            MAP_PLACES.append([j,i])

PLAYER_MOVE_FREQUENCY = 50 #ms
