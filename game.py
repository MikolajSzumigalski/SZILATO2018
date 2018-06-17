import pygame as pg
import numpy as np
import sys
from sprites import *
from map import *
from neural_network import NeuralNetwork
from game_logic import *
from os import path
from interface import *
from genetic import *
import copy
import knowledge_frames
import GeneticAlgorithm.genetic


available_modes = ["basic-genetic", "neural-networks", "decission-tree", "placing-genetic", "standard"]
class Game:
    def __init__(self, screen, mode="normal-genetic"):
        if not mode in available_modes:
            raise Exception("[game init] dany tryb (mode) nie jest znany, może zapomniałeś go dodać do 'available_modes'?")
        else:
            self.mode = mode
            print("\n[game init] #log game mode set to '" + mode + "'")
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        #init sprites and map
        self.all_sprites = pg.sprite.Group()
        self.monsters = []
        self.mixtures = []
        self.map = Map(self)
        self.map.load_from_file(MAP, RANDOM_SPAWN)

        if mode == "placing-genetic" :
            geneticImp = GeneticAlgorithmImplementation()
            geneticImp.run(self.map.map_data)

        self.player = Player(self, 1, 1)
        self.map_of_all = copy.deepcopy(self.map.legendReturn())
        self.dynamic_map = copy.deepcopy(self.map_of_all[:])
        self.dynamic_map = self.dynamic_map_update()
        self.inteface = Interface(self, self.player)
        self.inteface.draw_legend(self.dynamic_map)
        self.camera = Camera(self.map.camerawidth, self.map.cameraheight)
        #init music
        pg.mixer.init()
        bg_music = pg.mixer.music.load(path.join(music_folder, 'gamebackground.mp3'))
        self.logic_engine = LogicEngine(self)
        # pg.time.set_timer(self.MOVEEVENT, PLAYER_MOVE_FREQUENCY)
        if mode == "neural-networks" :
            network = NeuralNetwork(1,1,1)
            network.load_from(DEFAULT_NN)
            self.neural_network = network

        self.logic_attribute_name_list = ['monsters', 'mixtures', 'map', 'player', 'logic_engine', 'logic_attribute_name_list']
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.inteface.update(self.player)
        self.camera.update(self.player)
        self.dynamic_map = self.dynamic_map_update()


    def dynamic_map_update(self):
        dynamic_map = copy.deepcopy(self.map_of_all)
        for m in self.monsters:
            if m.alive:
                dynamic_map[m.y][m.x] = 2
        for m in self.mixtures:
            dynamic_map[m.y][m.x] = 3
        dynamic_map[self.player.y][self.player.x] = 4
        return dynamic_map

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.map.draw_grid(self.screen)
        #self.map.draw_map(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.inteface.draw_interface(self.screen)
        self.inteface.draw_legend(self.dynamic_map)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                # nie przyjmujemy nowych inputów podczas ruchu Geralta
                if not self.player.in_move:
                    if self.mode == "decission-tree":
                        if self.player.pausemove:
                            if event.key == pg.K_LEFT:
                            #sprawdź co się stanie jeśli player się przesunie
                                self.logic_engine.check_player_collisions(dx=-1)
                            if event.key == pg.K_RIGHT:
                                self.logic_engine.check_player_collisions(dx=1)
                            if event.key == pg.K_UP:
                                self.logic_engine.check_player_collisions(dy=-1)
                            if event.key == pg.K_DOWN:
                                self.logic_engine.check_player_collisions(dy=1)
                            if event.key == pg.K_w:
                                self.logic_engine.player_start_auto_move()
                        if not self.player.pausemove:
                            if event.key == pg.K_t:
                                 self.logic_engine.choose.atakuj(self.logic_engine.choose.tabMonster)
                            if event.key == pg.K_n:
                                 self.player.pausemove = True
                    else:
                        if event.key == pg.K_LEFT:
                        #sprawdź co się stanie jeśli player się przesunie
                            self.logic_engine.check_player_collisions(dx=-1)
                        if event.key == pg.K_RIGHT:
                            self.logic_engine.check_player_collisions(dx=1)
                        if event.key == pg.K_UP:
                            self.logic_engine.check_player_collisions(dy=-1)
                        if event.key == pg.K_DOWN:
                            self.logic_engine.check_player_collisions(dy=1)
                        if event.key == pg.K_w:
                            self.logic_engine.player_start_auto_move()

                        if event.key == pg.K_p:
                        # prints to file current map status in JSON form
                            knowledge_frames.save_data(self.logic_engine)

                        if event.key == pg.K_q:
                            #simulate going down 1
                            self.logic_engine.simulate_move(True, 0, 1)

                        if event.key == pg.K_g:
                            #simulate going down 1
                            self.logic_engine.simulate_move_absolute_coordinate(False, 1, 2);

                        if event.key == pg.K_a:
                            if not self.mode == "standard":
                                print("[game] #info if you want to use A*, switch game mode")
                            else: self.player.get_new_plan()

                        if event.key == pg.K_n:
                            if not self.mode == "neural-networks":
                                print("[game] #info if you want to use neural network, switch game mode")
                            else: self.logic_engine.nn_move()

                        if event.key == pg.K_0:
                            if not self.mode == "basic-genetic":
                                    print("[game] #info if you want to use genetic mikbal, switch game mode")
                            else:
                                GeneticAlgorithm.genetic.prepare_genetic(self.logic_engine)

                        if event.key == pg.K_9:
                            if not self.mode == "basic-genetic":
                                print("[game] #info if you want to use genetic mikbal, switch game mode")
                            else:
                                self.logic_engine.play_from_list([2, 0, 1, 7, 6, 8, 3, 0, 0, 8, 4, 9, 9, 4, 8, 1, 5, 2, 4, 1, 4, 8, 2, 5, 3, 7, 1, 5, 5, 0])
                                
            if event.type == pg.VIDEORESIZE:
                self.__resize_window__(event)
            if event.type == MOVEEVENT:
                self.logic_engine.player_auto_move()

    def get_monsters_positions(self, alive_only=False):
        out = []
        for m in self.monsters:
            if not alive_only: out.append([m.x, m.y])
            elif m.alive: out.append([m.x, m.y])
        return out

    def get_mixtures_positions(self, alive_only=False):
        out = []
        for m in self.mixtures:
            if not alive_only: out.append([m.x, m.y])
            elif m.alive: out.append([m.x, m.y])
        return out

    def get_tiles_around_player_simplified(self, n=1):
        """
        Get simplified matrix of states of tiles around player in ranges:
         x - n <= player_x <= x + n
         y - n <= player_y <= y + n
        Eg. for n = 1
        0  1  0
        0 -1  2
        1  1  2
        where:
        -2 - unknown tile (error)
         -1 - player (always in the center)
         0 - wall or another obstacle
         1 - unvisited tile
         2 - visited tile
         3 - monster tile
         4 - item tile
        """
        monsters = self.get_monsters_positions(alive_only=True)
        items = self.get_mixtures_positions(alive_only=True)
        out = np.zeros((2*n + 1, 2*n + 1), np.int8)
        temp_x = 0
        temp_y = 0
        for i in range(0, 2*n + 1):
            for j in range(0, 2*n + 1):
                temp_x = self.player.x + (i - n)
                temp_y = self.player.y + (j - n)

                if temp_x == self.player.x and temp_y == self.player.y:
                     out[j][i] = -1
                elif temp_x < 0 or temp_y < 0 or temp_x >= self.map.width or temp_y >= self.map.height:
                     out[j][i] = 0
                elif self.map.tiles_data[temp_y][temp_x].isCollidable:
                     out[j][i] = 0
                elif not self.map.tiles_data[temp_y][temp_x].isCollidable:
                    if self.map.tiles_data[temp_y][temp_x].visited: out[j][i] = 2
                    elif [temp_x, temp_y] in monsters: out[j][i] = 3
                    elif [temp_x, temp_y] in items: out[j][i] = 4
                    else:  out[j][i] = 1
                else: out[j][i] = -2
        return out


    def __resize_window__(self, event):
        """
        this handles resizing of a window, is called by events loop
        :param event, handled VIDEORESIZE pygame event"""
        #TODO ładne odświeżanie ekranu po rozszerzeniu powiększeniu
        WIDTH = event.w
        HEIGHT = event.h
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE);


    def __getstate__(self):
        state = self.__dict__.copy()
        newstate = {k: state[k] for k in self.logic_attribute_name_list}
        return newstate

    def __setstate__(self, state):
        self.__dict__.update(state)
