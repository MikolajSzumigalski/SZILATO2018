import pygame as pg
from settings import *
from abc import ABCMeta, abstractmethod
import os
import simplejson
from A_star import *
# import A_star

import program_logic
import jsonpickle

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
music_folder = os.path.join(game_folder, "music")

class Character(metaclass=ABCMeta):
    """ this is a general character abstract class that provides basis of drawing any character on screen"""
    def __init__(self, game, x, y, hp, at, deff, lev, exp, max_hp=0):

        # Atrybuty postaci LOGICZNE
        self.name = self.__class__.__name__
        self.id = id(self)
        self.x = x
        self.y = y
        self.hp = hp # punkty zdrowia
        self.at = at #atak
        self.deff = deff # obrona
        self.lev = lev # poziom
        self.total_exp = exp;
        self.max_hp = max_hp;
        self.alive = True
        if (self.max_hp == 0):
            self.max_hp = self.hp
        self.logic_attribute_name_list = ['logic_attribute_name_list' , 'name', 'id','hp', 'x', 'y', 'at', 'deff', 'lev', 'total_exp', 'max_hp', 'alive']

    # Te rzeczy są po to, by branie klasy i próbowanie jej wyprintowania etc. dawało tylko i wyłącznie
    # rzeczy logicznie (hp, exp etc), a nie grafiki i ten spam graficzny
    def __getstate__(self):
        state = self.__dict__.copy()
        newstate = {k: state[k] for k in self.logic_attribute_name_list}
        return newstate

    def __setstate__(self, state):
        self.__dict__.update(state)

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
        # self.visual_health_update()

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

    @abstractmethod
    def get_worth_exp(self):
        pass

class CharacterSprite(pg.sprite.Sprite):
    def __init__(self, character ,game):
        self.character = character
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.hbWidth = TILESIZE
        self.hbHeight = 6
        self.alpha = 255
        self.hbBase = pg.Surface((self.hbWidth, self.hbHeight))# 255 to max widoczność obrazka, 0 to pełne zaniknięcie
        self.fade_speed = 16     #prędkość zanikania
        self.fadepom = 0
        self.trans_value = 255

    def update(self):
        self.visual_health_update()
        self.hit_animation()

        self.rect.x = self.character.x * TILESIZE
        self.rect.y = self.character.y * TILESIZE

        self.character.window_x = self.rect.x
        self.character.window_y = self.rect.y

    def fade(self):
        self.fadepom = 1
        self.fade_direction = 1


    def visual_health_update(self):
        current_health_percentage = self.character.hp / self.character.max_hp
        if(current_health_percentage > 0):
            new_size = int(TILESIZE * current_health_percentage)
            width = new_size
            hb = pg.Surface((width, self.hbHeight))
            hb.fill(GREEN)

            self.hbBase.fill(RED)
            self.hbBase.blit(hb, (0,0))

            self.image.blit(self.hbBase, (5,45))

    def hit_animation(self):
        if(self.fadepom):
            if self.trans_value > 0 and self.fade_direction:
                if self.trans_value - self.fade_speed <= 0:
                    self.trans_value = 0
                    self.fade_direction = 0
                    #print(self.image.get_alpha())
                else:
                    self.trans_value = self.trans_value - self.fade_speed
                    #print(self.image.get_alpha())
            elif self.trans_value < 255:
                if self.trans_value + self.fade_speed >= 255:
                    self.trans_value = 255
                    self.fadepom = 0
                else:
                    self.trans_value = self.trans_value + self.fade_speed
        self.image.set_alpha(self.trans_value)

    def delete(self):
        pg.sprite.Sprite.remove(self, self.groups)
        # self.game.monsters.remove(self)

class Player(Character):
    """Player's implementation of Character class, that handles displaying Player's character on screen"""
    def __init__(self, game, x, y):
        #POZIOM 1
        hp = 70
        at = 70
        deff = 20
        lev = 1
        exp = 0 #punkty doświadczenia
        super(Player, self).__init__(game, x, y, hp, at, deff, lev, exp);
        PlayerSprite(self, game)
        self.in_move = False #czy gracz znajduje się w ruchu?
        self.next_steps = [] #zaplanowana droga, gdy coś tu jest in_move zmieni się na True
        self.game = game
        self.points_to_visit = []
        self.current_target = []

    def die(self, simulated = False):
        #TODO PROPER GAME ENDING
        # print("GAMEOVER")
        self.hp = 0
        self.at = 0
        self.max_hp = 0
        self.lev = 0
        self.deff = 0
        self.alive = False

    def get_new_path(self):
        A = A_star_path(self.game)
        self.current_target = self.points_to_visit.pop(0)
        self.next_steps = A.get_path_to(self.current_target)
        # print(self.next_steps)
        self.in_move = True

    def get_new_plan(self):
        A = A_star_target_list(self.game)
        temp = A.get_new_plan()
        pg.time.set_timer(MOVEEVENT, PLAYER_MOVE_FREQUENCY)
        for obj in temp:
            self.points_to_visit.append([obj.x, obj.y])
        print (self.points_to_visit)

    def update(self):
        pass

    def level_up(self):
        self.max_hp +=20
        self.at += 10
        self.deff += 10
        self.hp = self.max_hp
        self.lev += 1
        # print("level up, hp: {} totalexp: {} level{}".format(self.hp, self.total_exp, self.lev))
        # self.visual_health_update()
        pass

    def get_worth_exp(self):
        return 0

class PlayerSprite(CharacterSprite):
    def __init__(self, character, game):
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "geralt.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(PlayerSprite, self).__init__(character, game)


class Monster(Character, metaclass=ABCMeta):
    """Abstract class that provides implementation of Character class, that handles displaying a Monster on screen"""
    def __init__(self, game, x, y, hp, at, deff, lev):
        self.hp = hp # punkty zdrowia
        self.at = at #atak
        self.deff = deff # obrona
        self.lev = lev # poziom
        self.alive = True
        exp = 0
        super(Monster, self).__init__(game, x, y, hp, at, deff, lev, exp);

    def die(self):
        self.hp = 0
        self.alive = False
        # pg.sprite.Sprite.remove(self, self.groups)
        # self.game.monsters.remove(self)
        # del self


    def get_worth_exp(self):
        return sum([50 * level for level in range(1, self.lev + 1)])

    def level_up(self):
        pass

class MonsterSprite(CharacterSprite, metaclass=ABCMeta):
    def __init__(self, character, game):
        super(MonsterSprite, self).__init__(character, game)

    def update(self):
        self.visual_health_update()
        self.hit_animation()

        self.rect.x = self.character.x * TILESIZE
        self.rect.y = self.character.y * TILESIZE

        self.character.window_x = self.rect.x
        self.character.window_y = self.rect.y

        if not self.character.alive:
            self.delete()
            # pg.sprite.Sprite.remove(self, self.groups)
            # self.game.monsters.remove(self)




class Mglak(Monster):
    def __init__(self, game, x, y):
        #POZIOM 1
        hp = 50
        at = 60
        deff = 20
        lev = 1
        super(Mglak, self).__init__(game, x, y, hp, at, deff, lev);
        MglakSprite(self, game)

class MglakSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "mglak.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(MglakSprite, self).__init__(character, game)


class Spider(Monster):
    def __init__(self, game, x, y):
        #POZIOM 2
        hp = 100
        at = 80
        deff = 30
        lev = 2
        super(Spider, self).__init__(game, x, y, hp, at, deff, lev);
        SpiderSprite(self, game)

class SpiderSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "pajonk.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(SpiderSprite, self).__init__(character, game);

class Ghoul(Monster):
    def __init__(self, game, x, y):
        #POZIOM 3
        hp = 175
        at = 110
        deff = 40
        lev = 3
        super(Ghoul, self).__init__(game, x, y, hp, at, deff, lev);
        GhoulSprite(self, game)

class GhoulSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.image.load(os.path.join(img_folder, "ghoul.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(GhoulSprite, self).__init__(character, game);

class Leszy(Monster):
    def __init__(self, game, x, y):
        #POZIOM 4
        hp = 275
        at = 150
        deff = 50
        lev = 4
        super(Leszy, self).__init__(game, x, y, hp, at, deff, lev);
        LeszySprite(self, game)

class LeszySprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.image.load(os.path.join(img_folder, "leszy.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(LeszySprite, self).__init__(character, game);

class Olgierd(Monster):
    def __init__(self, game, x, y):
        #POZIOM 5
        hp = 400
        at = 200
        deff = 60
        lev = 5
        super(Olgierd, self).__init__(game, x, y, hp, at, deff, lev);
        OlgierdSprite(self, game)

class OlgierdSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.image.load(os.path.join(img_folder, "olgierd.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(OlgierdSprite, self).__init__(character, game);

class Dragon(Monster):
    def __init__(self, game, x, y):
        #POZIOM 6
        hp = 650
        at = 260
        deff = 70
        lev = 6
        super(Dragon, self).__init__(game, x, y, hp, at, deff, lev);
        DragonSprite(self, game)

class DragonSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.image.load(os.path.join(img_folder, "smok.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(DragonSprite, self).__init__(character, game);

class Gaunter(Monster):
    def __init__(self, game, x, y):
        #POZIOM 7
        hp = 800
        at = 350
        deff = 100
        lev = 7
        super(Gaunter, self).__init__(game, x, y, hp, at, deff, lev);
        GaunterSprite(self, game)

class GaunterSprite(MonsterSprite):
    def __init__(self, character, game):
        self.image = pg.image.load(os.path.join(img_folder, "gaunter.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        super(Gaunter, self).__init__(character, game);

class Item(metaclass=ABCMeta):
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.id = id(self)
        self.name = self.__class__.__name__
        self.logic_attribute_name_list = ['logic_attribute_name_list', 'name', 'id', 'x', 'y',
                                       'alive']

    # Te rzeczy są po to, by branie klasy i próbowanie jej wyprintowania etc. dawało tylko i wyłącznie
    # rzeczy logicznie (hp, exp etc), a nie grafiki i ten spam graficzny
    def __getstate__(self):
        state = self.__dict__.copy()
        newstate = {k: state[k] for k in self.logic_attribute_name_list}
        return newstate

    def __setstate__(self, state):
        self.__dict__.update(state)

    @abstractmethod
    def use(self, benefitor):
        pass

class HP_Mixture(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        HP_MixtureSprite(self, game, self.x,self.y )

    def use(self, benefitor):
        #TODO
        self.die()

    def die(self):
        self.alive = False

class HP_MixtureSprite(pg.sprite.Sprite):
    def __init__(self, character,  game, x, y):
        self.game = game
        self.character = character
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "red_elix.png")).convert()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if not self.character.alive:
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.mixtures.remove(self.character)
            del self





#class Ciri(pg.sprite.Sprite):
#    def __init__(self, game, x, y):
#        self.groups = game.all_sprites
#        pg.sprite.Sprite.__init__(self, self.groups)
#        self.game = game
#        self.rect = self.image.get_rect()
#        self.x = x
#        self.y = y
#        self.rect.x = self.x * TILESIZE
#        self.rect.y = self.y * TILESIZE

#class CiriSprite(CharacterSprite):
#    def __init__(self, character, game):
#        self.image = pg.Surface((TILESIZE, TILESIZE))
#        self.image = pg.image.load(os.path.join(img_folder, "ciri.png")).convert()
#        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
#        self.image.set_colorkey(WHITE)
#        super(PlayerSprite, self).__init__(character, game)
