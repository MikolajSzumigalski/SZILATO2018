#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg
from map import *
from game import *
import random
from os import path

#metody dla całej logiki gry (kolizje, eventy w grze itp.)

class LogicEngine:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.monsters = game.monsters
        self.map = game.map

    #sprawdź czy na nowym polu (new_x, new_y) wystąpi jakaś kolizja
    def check_player_collisions(self, dx=0, dy=0):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        print("player pos: ",new_x, new_y, " next_tile: ", self.map.map_data[new_y][new_x])
        #kolizje z potworami
        monster_collision = False
        for m in self.monsters:
            if new_x  == m.x and new_y == m.y:
                print("colision with monster!")
                monster_collision = True
                geralt_sounds = []
                for snd in ['geralt1.wav', 'geralt2.wav']:
                    geralt_sounds.append(pg.mixer.Sound(path.join(music_folder, snd)))
                #self.player.fight(m) - walkę można też realizować tutaj (np. w osobnej metodzie), a nie w playerze
                self.fight(self.player, m)
                random.choice(geralt_sounds).play()
        #kolizje ze ścianami
        if not monster_collision:
            collidables = [ROCK_1,ROCK_2,ROCK_3]
            if self.map.map_data[new_y][new_x] in collidables:
                print("collison with rock!")
            else:
                print("move")
                self.player.move(dx, dy)
                print(self.map.map_data[new_y][new_x])

    def fight(self, attacker, defender):
        '''
        this handles one turn of fighting in between characters
        :param charA: character enganging the fight
        :param charB: defender character
        :return:
        '''
        self.choose = self.chooseWeapon(self.game, attacker, defender, self)
        self.game.player.pausemove = False

    class chooseWeapon(pg.sprite.Sprite):
        def __init__(self ,game, attacker, defender, logic):
            self.groups = game.all_sprites
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.logic = logic
            self.attacker = attacker
            self.defender = defender
            self.image = pg.Surface((305,67))
            self.image = pg.image.load(os.path.join(img_folder, "bronie.png")).convert()
            self.image = pg.transform.scale(self.image, (610,134))
            self.rect = self.image.get_rect()
            self.rect.x = -self.game.camera.x -5
            self.rect.y = -self.game.camera.y + 50

        def silver(self):
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.player.pausemove = True
            starthp = self.game.player.hp
            for i in range(0, 1):
                if self.defender.fly == True or self.game.map.map_data[self.attacker.x][self.attacker.y] == '5':
                    print("Latam, lub jesteś w wodzie")
                    plik = open('przypadki.txt', 'a')
                    plik.writelines(
                    ["2 ",
                    str(-2000)+" ",
                    str(self.defender.fly)+" ",
                    self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                    str(self.defender.shield)+" ",
                    str(self.defender.monster)+" ",
                    str(0)+" ", str(-6)+ "\n"  ])
                    plik.close()
                    self.attacker.die()
                    return -2000
                if self.game.map.map_data[self.attacker.y][self.attacker.x] == '6':
                    print("Błoto")
                    self.attacker.hp -=3
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["2 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-3)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                if self.defender.shield == True:
                    print("Miałem tarczę")
                    self.attacker.hp -=2
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["2 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-2)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                if self.defender.monster == False:
                    print("Jestem człowiekiem XD")
                    self.attacker.hp -=2
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["2 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-2)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                self.attacker.points += 800
                self.defender.die()
                plik = open('przypadki.txt', 'a')
                plik.writelines(
                ["2 ",
                str(800)+" ",
                str(self.defender.fly)+" ",
                self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                str(self.defender.shield)+" ",
                str(self.defender.monster)+" ",
                str(self.attacker.hp)+" ", str(starthp-self.attacker.hp)+ "\n"  ])
                plik.close()
                return 800

        def stalowy(self):
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.player.pausemove = True
            starthp = self.game.player.hp
            for i in range(0, 1):
                if self.defender.fly == True or self.game.map.map_data[self.attacker.x][self.attacker.y] == '5':
                    print("Latam, lub jesteś w wodzie")
                    plik = open('przypadki.txt', 'a')
                    plik.writelines(
                    ["1 ",
                    str(-2000)+" ",
                    str(self.defender.fly)+" ",
                    self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                    str(self.defender.shield)+" ",
                    str(self.defender.monster)+" ",
                    str(0)+" ", str(-6)+ "\n"  ])
                    plik.close()
                    self.attacker.die()
                    return -2000
                if self.game.map.map_data[self.attacker.y][self.attacker.x] == '6':
                    print("Błoto")
                    self.attacker.hp -=3
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["1 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-3)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                if self.defender.shield == True:
                    print("Miałem tarczę")
                    self.attacker.hp -=2
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["1 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-2)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                if self.defender.monster == True:
                    print("Jestem potworem XD")
                    self.attacker.hp -=3
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["1 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-3)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                self.attacker.points += 1000
                self.defender.die()
                plik = open('przypadki.txt', 'a')
                plik.writelines(
                ["1 ",
                str(1000)+" ",
                str(self.defender.fly)+" ",
                self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                str(self.defender.shield)+" ",
                str(self.defender.monster)+" ",
                str(self.attacker.hp)+" ", str(starthp-self.attacker.hp)+ "\n"  ])
                plik.close()
                return 1000

        def bow(self):
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.player.pausemove = True
            starthp = self.game.player.hp
            for i in range(0, 1):
                if self.game.map.map_data[self.attacker.x][self.attacker.y] == '5':
                    print("Jesteś w wodzie")
                    plik = open('przypadki.txt', 'a')
                    plik.writelines(
                    ["4 ",
                    str(-2000)+" ",
                    str(self.defender.fly)+" ",
                    self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                    str(self.defender.shield)+" ",
                    str(self.defender.monster)+" ",
                    str(0)+" ", str(-6)+ "\n"  ])
                    plik.close()
                    self.attacker.die()
                    return -2000
                if self.defender.shield == True:
                    print("Miałem tarczę")
                    self.attacker.hp -=2
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["4 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-2)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                self.attacker.points += 400
                self.defender.die()
                plik = open('przypadki.txt', 'a')
                plik.writelines(
                ["4 ",
                str(400)+" ",
                str(self.defender.fly)+" ",
                self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                str(self.defender.shield)+" ",
                str(self.defender.monster)+" ",
                str(self.attacker.hp)+" ", str(starthp-self.attacker.hp)+ "\n"  ])
                plik.close()
                return 400


        def axe(self):
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.player.pausemove = True
            starthp = self.game.player.hp
            for i in range(0, 1):
                if self.defender.fly == True or self.game.map.map_data[self.attacker.x][self.attacker.y] == '5':
                    print("Latam, lub jesteś w wodzie")
                    plik = open('przypadki.txt', 'a')
                    plik.writelines(
                    ["3 ",
                    str(-2000)+" ",
                    str(self.defender.fly)+" ",
                    self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                    str(self.defender.shield)+" ",
                    str(self.defender.monster)+" ",
                    str(0)+" ", str(-6)+ "\n"  ])
                    plik.close()
                    self.attacker.die()
                    return -2000
                if self.game.map.map_data[self.attacker.x][self.attacker.y] == '6':
                    print("Błoto")
                    self.attacker.hp -=3
                    if self.attacker.hp <= 0:
                        plik = open('przypadki.txt', 'a')
                        plik.writelines(
                        ["3 ",
                        str(-2000)+" ",
                        str(self.defender.fly)+" ",
                        self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                        str(self.defender.shield)+" ",
                        str(self.defender.monster)+" ",
                        str(self.attacker.hp)+" ", str(-3)+ "\n"  ])
                        plik.close()
                        self.attacker.die()
                        return -2000
                self.attacker.points += 600
                self.defender.die()
                plik = open('przypadki.txt', 'a')
                plik.writelines(
                ["3 ",
                str(400)+" ",
                str(self.defender.fly)+" ",
                self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                str(self.defender.shield)+" ",
                str(self.defender.monster)+" ",
                str(self.attacker.hp)+" ", str(starthp-self.attacker.hp)+ "\n"  ])
                plik.close()
                return 600

        def fireball(self):
            pg.sprite.Sprite.remove(self, self.groups)
            starthp = self.game.player.hp
            self.game.player.pausemove = True
            for i in range(0, 1):
                if self.game.map.map_data[self.attacker.x][self.attacker.y] == '5':
                    print("Jesteś w wodzie")
                    plik = open('przypadki.txt', 'a')
                    plik.writelines(
                    ["5 ",
                    str(-2000)+" ",
                    str(self.defender.fly)+" ",
                    self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                    str(self.defender.shield)+" ",
                    str(self.defender.monster)+" ",
                    str(0)+" ", str(-6)+ "\n"  ])
                    plik.close()
                    self.attacker.die()
                    return -2000
                self.attacker.points += 200
                self.defender.die()
                plik = open('przypadki.txt', 'a')
                plik.writelines(
                ["5 ",
                str(200)+" ",
                str(self.defender.fly)+" ",
                self.game.map.map_data[self.attacker.y][self.attacker.x]+" ",
                str(self.defender.shield)+" ",
                str(self.defender.monster)+" ",
                str(self.attacker.hp)+" ", str(starthp-self.attacker.hp)+ "\n"  ])
                plik.close()
                return 200

        def mixture(self):
            pg.sprite.Sprite.remove(self, self.groups)
            self.game.player.pausemove = True
            self.game.player.hp = self.game.player.max_hp
            self.game.player.points -= (700)
