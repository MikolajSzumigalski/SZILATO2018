import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod

class Character(pg.sprite.Sprite, metaclass=ABCMeta):
    """ this is a general character abstract class that provides basis of drawing any character on screen"""
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
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
        color = YELLOW;
        super(Player, self).__init__(game, x, y, color);

class Monster(Character, metaclass=ABCMeta):
    """Abstract class that provides implementation of Character class, that handles displaying a Monster on screen"""
    def __init__(self, game, x, y):
        color = RED;
        super(Monster, self).__init__(game, x, y, color);

class Snake(Monster):
    """Example implementation of Abstract class, that handles displaying a Snake character on screen"""
    pass;
