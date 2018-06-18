#THIS FILE IS RESPONSIBLE FOR MANAGING BIG PICTURE PROGRAM LOGIC
#e.g: start menu, starting the proper game

import pygame as pg
from settings import *
from game import *
from intro import *
<<<<<<< HEAD
<<<<<<< HEAD
from train_nn import *
=======
>>>>>>> parent of 85e25b3... add nn trainig stage function
=======
>>>>>>> parent of 85e25b3... add nn trainig stage function
#tworzymy okno
#wyświetlamy menu
#startujemy grę

def startup():
    """ this starts the entire program"""
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
    intro = Intro(screen)
    mode = intro.run()
<<<<<<< HEAD
<<<<<<< HEAD
    temp_mode = mode
    if mode == 'neural-networks-training':
         network = train_network(screen)
         mode = 'neural-networks'

=======
>>>>>>> parent of 85e25b3... add nn trainig stage function
=======
>>>>>>> parent of 85e25b3... add nn trainig stage function
    print("-----START GAME------")
    game = Game(screen, mode)
    if temp_mode == 'neural-networks-training': game.set_network(network)
    game.run()

def gameover():
    """ this handles gameover """
    print("Game Over")
    startup()
