#THIS FILE IS RESPONSIBLE FOR MANAGING BIG PICTURE PROGRAM LOGIC
#e.g: start menu, starting the proper game

import pygame as pg
from settings import *
from game import *
#tworzymy okno
#wyświetlamy menu
#startujemy grę

def startup():
    """ this starts the entire program"""
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
    #TO DO: przejście do menu, można np. dodać metodę z osobną pętlą.
    game = Game(screen)
    game.run()

def gameover():
    """ this handles gameover """
    startup()
