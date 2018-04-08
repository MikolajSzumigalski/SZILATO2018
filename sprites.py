import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Character(pg.sprite.Sprite, metaclass=ABCMeta):
    """ this is a general character abstract class that provides basis of drawing any character on screen"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def teleport(self, new_x, new_y):
        """
        this teleports Character to a new position
        :param new_x: new x coordinate
        :param new_y: new y coordinate
        """
        self.x = new_x
        self.y = new_y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Player(Character):
    """Player's implementation of Character class, that handles displaying Player's character on screen"""
    def __init__(self, game, x, y):
        self.image = pg.image.load(os.path.join(img_folder, "geralt.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Player, self).__init__(game, x, y);

class Monster(Character, metaclass=ABCMeta):
    """Abstract class that provides implementation of Character class, that handles displaying a Monster on screen"""
    def __init__(self, game, x, y):
        self.image = pg.image.load(os.path.join(img_folder, "gaunter.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Monster, self).__init__(game, x, y);

class Snake(Monster):
    """Example implementation of Abstract class, that handles displaying a Snake character on screen"""
    pass;
