import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod
import os
import random

import program_logic

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
music_folder = os.path.join(game_folder, "music")

class Character(pg.sprite.Sprite, metaclass=ABCMeta):
    """ this is a general character abstract class that provides basis of drawing any character on screen"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hbWidth = TILESIZE
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
            new_size = int(TILESIZE * current_health_percentage)
            width = new_size
            hb = pg.Surface((width, self.hbHeight))
            hb.fill(GREEN)

            self.hbBase.fill(RED)
            self.hbBase.blit(hb, (0,0))

            self.image.blit(self.hbBase, (5,45))

    def update(self):
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
                    self.fadepom = 0
                else:
                    self.trans_value = self.trans_value + self.fade_speed
        self.image.set_alpha(self.trans_value)

    @abstractmethod
    def die(self):
        pass

class Player(Character):
    """Player's implementation of Character class, that handles displaying Player's character on screen"""
    def __init__(self, game, x, y):
        #POZIOM 1
        self.hp = 6
        self.max_hp = 6
        self.points = 0
        self.pausemove = True
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "geralt.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Player, self).__init__(game, x, y);

    def die(self):
        #TODO PROPER GAME ENDING
        self.x = 1
        self.y = 1
        self.hp = 6
        self.points += -2000

    def update(self):
        self.visual_health_update()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Monster(Character, metaclass=ABCMeta):
    """Abstract class that provides implementation of Character class, that handles displaying a Monster on screen"""
    def __init__(self, game, x, y):
        pom = random.randint(0,3)
        if pom != 1:
            pom = 0
        self.shield = pom
        self.armour = random.randint(0,1)
        super(Monster, self).__init__(game, x, y);

    def die(self):
        pg.sprite.Sprite.remove(self, self.groups)
        self.game.monsters.remove(self)
        del self

class Mglak(Monster):
    def __init__(self, game, x, y):
        self.human = False
        self.monster = True
        self.fly = False
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "mglak.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Mglak, self).__init__(game, x, y);

class Spider(Monster):
    def __init__(self, game, x, y):
        self.human = False
        self.monster = True
        self.fly = False
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "pajonk.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Spider, self).__init__(game, x, y);

class Ghoul(Monster):
    def __init__(self, game, x, y):
        self.monster = True
        self.fly = False
        self.image = pg.image.load(os.path.join(img_folder, "ghoul.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Ghoul, self).__init__(game, x, y);

class Leszy(Monster):
    def __init__(self, game, x, y):
        self.monster = True
        self.fly = False
        self.image = pg.image.load(os.path.join(img_folder, "leszy.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Leszy, self).__init__(game, x, y);

class Olgierd(Monster):
    def __init__(self, game, x, y):
        self.monster = False
        self.fly = False
        self.image = pg.image.load(os.path.join(img_folder, "olgierd.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Olgierd, self).__init__(game, x, y);

class Dragon(Monster):
    def __init__(self, game, x, y):
        self.monster = True
        self.fly = True
        self.image = pg.image.load(os.path.join(img_folder, "smok.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Dragon, self).__init__(game, x, y);

class Gaunter(Monster):
    def __init__(self, game, x, y):
        self.monster = False
        self.fly = True
        self.image = pg.image.load(os.path.join(img_folder, "gaunter.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Gaunter, self).__init__(game, x, y);
