#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg
from map import *
from game import *
from A_star import *
import random
from os import path



#metody dla całej logiki gry (kolizje, eventy w grze itp.)
class LogicEngine:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.monsters = game.monsters
        self.mixtures = game.mixtures
        self.map = game.map

    #sprawdź czy na nowym polu (new_x, new_y) wystąpi jakaś kolizja
    def check_player_collisions(self, dx=0, dy=0):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        print("player pos: ",new_x, new_y, " next_tile: ", self.map.map_data[new_y][new_x])
        #kolizje z potworami
        monster_collision = False
        mixture_collision = False
        for m in self.monsters:
            if new_x  == m.x and new_y == m.y:
                print("colision with monster!")
                monster_collision = True
                geralt_sounds = []
                for snd in ['geralt1.wav', 'geralt2.wav']:
                    geralt_sounds.append(pg.mixer.Sound(path.join(music_folder, snd)))
                random.choice(geralt_sounds).play()
                #self.player.fight(m) - walkę można też realizować tutaj (np. w osobnej metodzie), a nie w playerze
                self.fight(self.player, m)
        #kolizje ze ścianami
        for m in self.mixtures:
            if new_x  == m.x and new_y == m.y:
                print("Let's drink!")
                mixture_collision = True
                self.player.hp = self.player.max_hp
                m.die()
        if not monster_collision and not mixture_collision:
            collidables = [ROCK_1,ROCK_2,ROCK_3,WATER]
            if self.map.map_data[new_y][new_x] in collidables:
                print("collison with rock or water!")
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

        for current_attacker, current_defender in zip([attacker, defender], [defender, attacker]):
            if(current_attacker.at > current_defender.deff):
                print(current_defender.hp)
                current_defender.take_damage(current_attacker.at - current_defender.deff)
                print(current_defender.hp)
            if(current_defender.hp <= 0):
                exp_to_be_given = current_defender.get_worth_exp()
                print("EXP TO BE GIVEN", exp_to_be_given)
                current_attacker.add_exp(exp_to_be_given)
                current_defender.die();
                break
            else:
                current_defender.fade()

    def player_auto_move(self):
        #obsługa auto-ruchu bohatera, zaplanowana droga znajduje się w player.next_steps
        if self.player.in_move:
            print(self.player.next_steps)

            if not self.player.next_steps:
                self.player.in_move = False

            else:
                next_tile = self.player.next_steps.pop(0)
                dx = next_tile[0] - self.player.x
                dy = next_tile[1] - self.player.y

                if not dx in [-1, 0, 1] or not dy in [-1, 0, 1]:
                    print("[Player auto move] tile ", next_tile, " too far from ", self.player.x, self.player.y)
                    self.player.next_steps = []
                else:
                    self.check_player_collisions(dx, dy)

    def player_start_auto_move(self):
        # funkcja głównie do debugowania
        dest = list(map(int, input("move to: ").split()))
        A = A_star(self.game)
        path = A.get_path_to(dest)
        self.player.in_move = True
        self.player.next_steps = path
        pg.time.set_timer(self.game.MOVEEVENT, PLAYER_MOVE_FREQUENCY)
