import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod
import os

import program_logic

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Character(pg.sprite.Sprite, metaclass=ABCMeta):
    """ this is a general character abstract class that provides basis of drawing any character on screen"""
    def __init__(self, game, x, y, hp, at, deff, lev, exp, max_hp=0):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #Atrybuty postaci
        self.hp = hp # punkty zdrowia
        self.at = at #atak
        self.deff = deff # obrona
        self.lev = lev # poziom
        self.exp = exp;
        self.max_hp = max_hp;
        if (self.max_hp == 0):
            self.max_hp = self.hp

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

    def take_damage(self, damage):
        '''
        this function handles taking raw number of damage to the character and plays damage animation
        :param damage:
        :return:
        '''
        self.hp -= damage
        current_health_percentage = self.hp / self.max_hp
        if(current_health_percentage > 0):
            new_size = int(32 * current_health_percentage)
            self.image = pg.transform.scale(self.image, (new_size, new_size))


    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def add_exp(self, exp):
        self.exp += exp;
        #TODO

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def level_up(self):
        pass

class Player(Character):
    """Player's implementation of Character class, that handles displaying Player's character on screen"""
    def __init__(self, game, x, y):
        #POZIOM 1
        hp = 70
        at = 70
        deff = 20
        lev = 1
        exp = 0 #punkty doświadczenia
        self.image = pg.image.load(os.path.join(img_folder, "geralt.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Player, self).__init__(game, x, y, hp, at, deff, lev, exp);

    def die(self):
        #TODO PROPER GAME ENDING
        print("GAMEOVER")
        program_logic.gameover()

    def level_up(self):
        #TODO LEVEL UP
        pass


class Monster(Character, metaclass=ABCMeta):
    """Abstract class that provides implementation of Character class, that handles displaying a Monster on screen"""
    def __init__(self, game, x, y, hp, at, deff, lev):
        self.hp = hp # punkty zdrowia
        self.at = at #atak
        self.deff = deff # obrona
        self.lev = lev # poziom
        exp = 0
        super(Monster, self).__init__(game, x, y, hp, at, deff, lev, exp);

    def die(self):
        self.hp = 0
        pg.sprite.Sprite.remove(self, self.groups)
        self.game.monsters.remove(self)
        del self

    def level_up(self):
        pass

class Mglak(Monster):
    def __init__(self, game, x, y):
        #POZIOM 1
        hp = 50
        at = 60
        deff = 20
        lev = 1
        self.image = pg.image.load(os.path.join(img_folder, "mglak.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Mglak, self).__init__(game, x, y, hp, at, deff, lev);

class Spider(Monster):
    def __init__(self, game, x, y):
        #POZIOM 2
        hp = 100
        at = 80
        deff = 30
        lev = 2
        self.image = pg.image.load(os.path.join(img_folder, "pajonk.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Spider, self).__init__(game, x, y, hp, at, deff, lev);

class Leszy(Monster):
    def __init__(self, game, x, y):
        #POZIOM 3
        hp = 175
        at = 110
        deff = 40
        lev = 3
        self.image = pg.image.load(os.path.join(img_folder, "leszy.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Leszy, self).__init__(game, x, y, hp, at, deff, lev);
