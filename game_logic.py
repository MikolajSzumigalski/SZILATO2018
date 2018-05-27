#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg
from map import *
from game import *
from A_star import *
import copy
import random
import knowledge_frames
from os import path



#metody dla całej logiki gry (kolizje, eventy w grze itp.)
class LogicEngine:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.monsters = game.monsters
        self.items = game.items
        self.map = game.map
        self.logic_attribute_name_list = ['player', 'monsters', 'items', 'map', 'gameover', 'simulation', 'logic_attribute_name_list']
        # self.gameover = False
        self.simulation = False

    #sprawdź czy na nowym polu (new_x, new_y) wystąpi jakaś kolizja
    def check_player_collisions(self, dx=0, dy=0, simulation = False, absolute_coordinates = False):
        if(absolute_coordinates):
            new_x = dx
            new_y = dy
        else:
            new_x = self.player.x + dx
            new_y = self.player.y + dy
        # print("player pos: ",new_x, new_y, " next_tile: ", self.map.map_data[new_y][new_x])
        #kolizje z potworami
        monster_collision = False
        mixture_collision = False
        for m in self.monsters:
            if new_x  == m.x and new_y == m.y and m.alive:
                monster_collision = True
                # print("colision with monster!")
                if not (simulation):
                    geralt_sounds = []
                    for snd in ['geralt1.wav', 'geralt2.wav']:
                        geralt_sounds.append(pg.mixer.Sound(path.join(music_folder, snd)))
                    random.choice(geralt_sounds).play()
                self.fight(self.player, m)
        #kolizje ze ścianami
        # print(self.items)
        for i in self.items:
            if new_x  == i.x and new_y == i.y and i.alive:
                i.use(self.player)
                mixture_collision = True
                self.map.tiles_data[i.x][i.y].setOccupiedBy(None);
                break

        if not monster_collision and not mixture_collision:
            collidables = [ROCK_1,ROCK_2,ROCK_3,WATER]
            if not self.map.map_data[new_y][new_x] in collidables:
                self.map.tiles_data[self.player.x][self.player.y].setOccupiedBy(None);
                self.map.tiles_data[dx][dy].setOccupiedBy(self.player);

                self.player.move(dx, dy)

        self.check_gameover()

    def fight(self, attacker, defender):
        '''
        this handles one turn of fighting in between characters
        :param charA: character enganging the fight
        :param charB: defender character
        :return:
        '''

        for current_attacker, current_defender in zip([attacker, defender], [defender, attacker]):
            if(current_attacker.get_total_at() > current_defender.get_total_deff()):
                # print(current_defender.hp)
                print("attacker AT:",current_attacker.get_total_at())
                print("attacker DEF:",current_attacker.get_total_deff(),"\n")
                current_defender.take_damage(current_attacker.get_total_at() - current_defender.get_total_deff())
                # print(current_defender.hp)
            if(current_defender.hp <= 0):
                exp_to_be_given = current_defender.get_worth_exp()
                # print("EXP TO BE GIVEN", exp_to_be_given)
                current_attacker.add_exp(exp_to_be_given)
                if current_attacker == attacker:
                    self.map.tiles_data[attacker.x][attacker.y].setOccupiedBy(None);
                    attacker.x = current_defender.x
                    attacker.y = current_defender.y
                    self.map.tiles_data[attacker.x][attacker.y].setOccupiedBy(attacker);

                current_defender.die();
                self.check_gameover()
                break
            # else:
                # current_defender.fade()

    def player_auto_move(self):
        #obsługa auto-ruchu bohatera, zaplanowana droga znajduje się w player.next_steps
        # if not self.player.points_to_visit:
        #     self.player.get_new_plan()
        #     A = A_star_target_list(self.game)
        #     temp = A.get_new_plan()
        #     temp_new_plan = []
        #     for obj in temp:
        #         temp_new_plan.append([obj.x, obj.y])
        #     self.player.points_to_visit = temp_new_plan

        if self.player.in_move:

            if not self.player.next_steps:
                self.player.in_move = False

            else:
                next_tile = self.player.next_steps.pop(0)
                dx = next_tile[0] - self.player.x
                dy = next_tile[1] - self.player.y

                if not dx in [-1, 0, 1] or not dy in [-1, 0, 1]:
                    # print("[Player auto move] tile ", next_tile, " too far from ", self.player.x, self.player.y)
                    self.player.next_steps = []
                else:
                    self.check_player_collisions(dx, dy)
        else:
            if self.player.points_to_visit:
                self.player.get_new_path()
        # print(self.player.points_to_visit)

    def player_start_auto_move(self):
        # funkcja głównie do debugowania
        dest = list(map(int, input("move to: ").split()))
        A = A_star_path(self.game)
        path = A.get_path_to(dest)
        self.player.in_move = True
        self.player.next_steps = path
        # pg.time.set_timer(self.game.MOVEEVENT, PLAYER_MOVE_FREQUENCY)



    def simulate_action(self, function_name, save_simulated_state_JSON = False, *args, **kwargs):
        """
        this method simulates behaviour of any of the LogicEngine methods without actually executing them in the game
        :param function_name:
        :param args:
        :param kwargs:
        :return: simulated game state
        """
        simulated_logic_engine = copy.deepcopy(self)
        simulated_logic_engine.simulation = True
        method_to_call = getattr(simulated_logic_engine, function_name)
        method_to_call(*args, **kwargs)
        simulated_logic_engine.check_gameover()
        if(save_simulated_state_JSON):
            knowledge_frames.save_data(simulated_logic_engine, "simulated_frames.json")
        return simulated_logic_engine

    def simulate_move(self,  save_simulated_state_JSON = False, dx=0, dy=0):
        """ simulates player's move by +-dx, +-dy coordinates """
        return self.simulate_action('check_player_collisions', save_simulated_state_JSON, dx, dy, simulation=True)

    def simulate_move_absolute_coordinate(self,  save_simulated_state_JSON = False, x=0, y=0):
        """ simulates player's move onto absolute dx, dy coordinates """
        return self.simulate_action('check_player_collisions', save_simulated_state_JSON, x, y, simulation=True, absolute_coordinates = True)

    def check_gameover(self):
        if self.player.hp <= 0 or not self.game.get_alive_monsters():
            # self.gameover = True
            if(self.simulation == True):
                pass
            else:
                self.game.gameover = True

    # # Te rzeczy są po to, by branie klasy i próbowanie jej kopiowania dało tylko
    # # rzeczy logicznie (hp, exp etc), a nie grafiki i ten spam graficzny
    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     newstate = {k: state[k] for k in self.logic_attribute_name_list}
    #     return newstate
    #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)
