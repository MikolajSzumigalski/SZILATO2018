import os
import pygame as pg
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

#MAP = "labirynt_szumi_deluxe.map"
#MAP = "NN_test.map"
MAP = "test.map"
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
RANDOM_SPAWN = False
MOVEEVENT = pg.USEREVENT+1
for i in range (0, GRIDHEIGHT):
    for j in range (0, GRIDWIDTH):
        if MAPLIST[i][j] == ".":
            MAP_PLACES.append([j,i])

PLAYER_MOVE_FREQUENCY = 100 #ms

#NN SETTINGS

DEFAULT_NN = "networks/best_new.npy"

NN_GENERATION_SIZE = 50
NN_INPUTS = 24
NN_POSSIBLE_STATES = 5
NN_HIDDEN_LAYER_SIZE = 50
NN_ROUNDS = 130
NN_MOVES = 40
NN_CROS_PROB = 0.3
NN_MUTATION_PROB = 0.01
NN_CROSS_TYPE = "means"
NN_FILENAME = "out_3.npy"
NN_LOGS_FILENAME = "last_training_logs.dat"
NN_FIRST_PRIZE = 2
NN_TARGET_SCORE = 1700
