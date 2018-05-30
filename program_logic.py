#THIS FILE IS RESPONSIBLE FOR MANAGING BIG PICTURE PROGRAM LOGIC
#e.g: start menu, starting the proper game

import pygame as pg
from settings import *
from game import *
from intro import *
#tworzymy okno
#wyświetlamy menu
#startujemy grę

def startup():
    """ this starts the entire program"""
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
    # intro = Intro(screen)
    # intro.run()
    game_1 = Game(screen)
    game_1.set_mode("normal", 50)
    print("GAME SCORE: ",game_1.run())
    game_2 = Game(screen)
    game_2.set_mode("normal", 50)
    print("GAME SCORE: ",game_2.run())

    # gameover()

def gameover():
    """ this handles gameover """
    startup()
