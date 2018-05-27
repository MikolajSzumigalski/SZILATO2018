import pygame as pg
import sys
from sprites import *
from map import *
from game_logic import *
from os import path
from interface import *

import copy
import knowledge_frames
class Game:
    def __init__(self, screen):
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

        self.logic_attribute_name_list = ['monsters', 'items', 'map', 'player', 'logic_engine', 'logic_attribute_name_list']
        self.gameover = False

    def run(self):
        # game loop - set self.playing = False to end the game
        # self.playing = True
        pg.mixer.music.play()
        while not self.gameover:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
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
