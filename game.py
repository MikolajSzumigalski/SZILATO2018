import pygame as pg
import sys
from sprites import *
from map import *
from game_logic import *
from os import path
from interface import *
import numpy as np

import copy
import knowledge_frames
class Game:
    def __init__(self, screen, no_graphics=False):
        self.no_graphics = no_graphics
        if no_graphics:
            # self.screen = screen
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
            pg.key.set_repeat(500, 100)
            #init sprites and map
            # self.all_sprites = pg.sprite.Group()
            self.monsters = []
            self.items = []
            self.map = Map(self, True)
            self.map.load_from_file(MAP, RANDOM_SPAWN)
            self.player = Player(self, 1, 1)
            self.map_of_all = copy.deepcopy(self.map.legendReturn())
            # self.dynamic_map = copy.deepcopy(self.map_of_all[:])
            # self.dynamic_map = self.dynamic_map_update()
            # self.inteface = Interface(self, self.player)
            # self.inteface.draw_legend(self.dynamic_map)
            # self.camera = Camera(self.map.camerawidth, self.map.cameraheight)
            #init music
            # pg.mixer.init()
            # bg_music = pg.mixer.music.load(path.join(music_folder, 'gamebackground.mp3'))
            self.logic_engine = LogicEngine(self)
            # pg.time.set_timer(self.MOVEEVENT, PLAYER_MOVE_FREQUENCY)

            self.logic_attribute_name_list = ['monsters', 'items', 'map', 'player', 'logic_engine', 'logic_attribute_name_list']
            self.gameover = False
            self.all_modes = ["normal", "auto-random", "auto-a-star"]
            self.mode = "normal"
            self.steps = -1

        else:
            self.mode = "normal"
            self.screen = screen
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
            pg.key.set_repeat(500, 100)
            #init sprites and map
            self.all_sprites = pg.sprite.Group()
            self.monsters = []
            self.items = []
            self.map = Map(self)
            self.map.load_from_file(MAP, RANDOM_SPAWN)

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

            self.logic_attribute_name_list = ['mode','monsters', 'items', 'map', 'player', 'logic_engine', 'logic_attribute_name_list']
            self.gameover = False
            self.all_modes = ["normal", "auto-random", "auto-a-star"]
            self.steps = -1

    def set_mode(self, mode, steps=100):
        if mode in self.all_modes:
            self.mode = mode
            self.steps = steps
            print("game mode switched to: '" + str(mode) + "'")
        else:
            print("this mode is not known: '" + str(mode) + "'")


    def run(self):
        # game loop - set self.playing = False to end the game
        # self.playing = True
        print("GAME START")
        if not self.no_graphics: pg.mixer.music.play()
        while not self.gameover:
            self.dt = self.clock.tick(FPS) / 1000
            if self.mode == "auto-random":
                self.events()
                self.logic_engine.auto_run()
                if not self.no_graphics:
                    self.draw()
                    self.update()
            else:
                self.events()
                if not self.no_graphics:
                     self.draw()
                     self.update()

        print("GAME END")
        return self.player.score

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
        for m in self.items:
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
                        # self.logic_engine.player_start_auto_move()
                        self.logic_engine.auto_run()

                    if event.key == pg.K_p:
                    # prints to file current map status in JSON form
                        knowledge_frames.save_data(self.logic_engine)

                    if event.key == pg.K_q:
                        #simulate going down 1
                        # self.logic_engine.simulate_move(True, 0, 1)
                        print(self.get_tiles_around_player_simplified(2))

                    # if event.key == pg.K_g:
                    #     #simulate going down 1
                    #     self.logic_engine.simulate_move_absolute_coordinate(False, 1, 2);

                    if event.key == pg.K_a:
                         self.player.get_new_plan()

            if event.type == pg.VIDEORESIZE:
                self.__resize_window__(event)
            if event.type == MOVEEVENT:
                self.logic_engine.player_auto_move()

    def get_monsters_positions(self):
        out = []
        for m in self.monsters:
            out.append([m.x, m.y])
        return out

    def get_items_positions(self):
        out = []
        for m in self.items:
            out.append([m.x, m.y])
        return out

    def get_alive_monsters(self):
        out = []
        for m in self.monsters:
            if m.alive: out.append(m)
        return out

    def get_alive_items(self):
        out = []
        for i in self.items:
            if i.alive: out.append(i)
        return out

    def get_alive_monsters_positions(self):
        out = []
        for m in self.monsters:
            if m.alive: out.append(m)
        return out

    def get_alive_items_positions(self):
        out = []
        for i in self.items:
            if i.alive: out.append(i)
        return out


    def __resize_window__(self, event):
        """
        this handles resizing of a window, is called by events loop
        :param event, handled VIDEORESIZE pygame event"""
        #TODO ładne odświeżanie ekranu po rozszerzeniu powiększeniu
        WIDTH = event.w
        HEIGHT = event.h
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE);

    def get_tiles_around_player_simplified(self, n=1):
        """
        Get simplified matrix of states of tiles around playerself in ranges:
         x - n <= player_x <= x + n
         y - n <= player_y <= y + n
        Eg. for n = 2
        11111
        00100
        00x22
        01122
        01220
        222
        where:
         -1 - player (always in the center)
         0 - wall or another obstacle
         1 - unvisited tile
         2 - visited tile
        """
        monsters_and_items_positions = self.get_monsters_positions() + self.get_items_positions()
        out = np.zeros((2*n + 1, 2*n + 1))
        temp_x = 0
        temp_y = 0
        for i in range(0, 2*n + 1):
            for j in range(0, 2*n + 1):
                temp_x = self.player.x + (i - n)
                temp_y = self.player.y + (j - n)
                print(temp_x, temp_y, i, j)
                if temp_x == self.player.x and temp_y == self.player.y:
                    out[j][i] = -1
                    continue
                elif temp_x < 0 or temp_y < 0 or temp_x >= self.map.width or temp_y >= self.map.height:
                    out[j][i] = 0
                    print("here")
                    continue
                elif self.map.tiles_data[temp_y][temp_x].isCollidable:
                    out[j][i] = 0
                    continue
                elif not self.map.tiles_data[temp_y][temp_x].isCollidable:
                    if self.map.tiles_data[temp_y][temp_x].visited: out[j][i] = 2
                    else: out[j][i] = 1 
                    continue
                else:
                    out[j][i] = -2

        return out

    def get_tiles_around_player(self, n=1):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        newstate = {k: state[k] for k in self.logic_attribute_name_list}
        return newstate

    def __setstate__(self, state):
        self.__dict__.update(state)
