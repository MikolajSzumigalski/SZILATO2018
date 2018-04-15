import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod
import os

import program_logic

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
music_folder = os.path.join(game_folder, "music")

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
        self.total_exp = exp;
        self.max_hp = max_hp;
        if (self.max_hp == 0):
            self.max_hp = self.hp
        self.hbWidth = 32
        self.hbHeight = 6
        self.alpha = 255
        self.hbBase = pg.Surface((self.hbWidth, self.hbHeight))
        # 255 to max widoczność obrazka, 0 to pełne zaniknięcie
        #prędkość zanikania
        self.fade_speed = 16
        self.fadepom = 0
        self.trans_value = 255

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
        self.visual_health_update()
    def fade(self):
        self.fadepom = 1
        self.fade_direction = 1


    def visual_health_update(self):
        #TODO TAKE DAMAGE GUYS
        current_health_percentage = self.hp / self.max_hp
        if(current_health_percentage > 0):
            new_size = int(32 * current_health_percentage)
            width = new_size
            hb = pg.Surface((width, self.hbHeight))
            hb.fill(GREEN)

            self.hbBase.fill(RED)
            self.hbBase.blit(hb, (0,0))

            self.image.blit(self.hbBase, (3,29))

    def update(self):
        self.visual_health_update()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        if(self.fadepom):
            if self.trans_value > 0 and self.fade_direction:
                if self.trans_value - self.fade_speed <= 0:
                    self.trans_value = 0
                    self.fade_direction = 0
                    print(self.image.get_alpha())
                else:
                    self.trans_value = self.trans_value - self.fade_speed
                    print(self.image.get_alpha())
            elif self.trans_value < 255:
                if self.trans_value + self.fade_speed >= 255:
                    self.trans_value = 255
                    print(self.image.get_alpha())
                    self.fadepom = 0
                else:
                    self.trans_value = self.trans_value + self.fade_speed
                    print(self.image.get_alpha())
        self.image.set_alpha(self.trans_value)

    @abstractmethod
    def level_up(self):
        pass;

    def add_exp(self, exp):
        self.total_exp += exp;
        while self.total_exp >= sum([100 * level for level in range(1, self.lev+1)]):
             self.level_up();
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
        self.image = pg.Surface((32, 32))
        self.image = pg.image.load(os.path.join(img_folder, "geralt.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        super(Player, self).__init__(game, x, y, hp, at, deff, lev, exp);

    def die(self):
        #TODO PROPER GAME ENDING
        print("GAMEOVER")
        program_logic.gameover()

    def level_up(self):
        self.max_hp +=20
        self.at += 10
        self.deff += 10
        self.hp = self.max_hp
        self.lev += 1
        print("level up, hp: {} totalexp: {} level{}".format(self.hp, self.total_exp, self.lev))
        self.visual_health_update()
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
        self.image = pg.Surface((32, 32))
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
        self.image = pg.Surface((32, 32))
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
