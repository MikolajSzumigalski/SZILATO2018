#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg
from map import *


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
                self.fight(self.player, m)
        #kolizje ze ścianami
        if not monster_collision:
            collidables = [ROCK_1, ROCK_2, ROCK_3, WATER]
            if self.map.map_data[new_y][new_x] in collidables:
                print("collison with rock or water!")
            else:
                print("move")
                self.player.move(dx, dy)

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
                current_defender.die()
                #TODO DODAWANIE EXP
                # attacker.add_exp(0)
                break






