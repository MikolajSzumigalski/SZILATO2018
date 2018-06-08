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
    intro = Intro(screen)
    mode = intro.run()
    print("-----START GAME------")
    game = Game(screen, mode)
    game.run()

def gameover():
    """ this handles gameover """
    print("Game Over")
    startup()
