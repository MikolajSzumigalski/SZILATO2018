import pygame as pg
import sys
from sprites import *
from map import *
from game_logic import *
from os import path
from interface import *
import random
import copy
class Game:
    def __init__(self, screen):
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        #init sprites and map
        self.all_sprites = pg.sprite.Group()
        self.monsters = []
        self.map = Map(self)
        self.map.load_from_file(MAP)
        self.map.init_tile_objects()
        for i in range (0, 10):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Mglak(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 8):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Spider(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 6):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Ghoul(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 5):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Leszy(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 4):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Olgierd(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

        for i in range (0, 3):
            rand = random.randint(0, len(MAP_PLACES)-1)
            self.monsters.append(Dragon(self, MAP_PLACES[rand][0], MAP_PLACES[rand][1]))
            MAP_PLACES.remove(MAP_PLACES[rand])

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

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.pause = True
        pg.mixer.music.play()
        while self.playing:
            while self.pause:
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


    def dynamic_map_update(self):
        dynamic_map = copy.deepcopy(self.map_of_all)
        for m in self.monsters:
            dynamic_map[m.y][m.x] = 2
        dynamic_map[self.player.y][self.player.x] = 4
        return dynamic_map

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.map.draw_grid(self.screen)
        #self.map.draw_map(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.inteface.draw_interface(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if self.player.pausemove:
                    if event.key == pg.K_LEFT:
                        #sprawdź co się stanie jeśli player się przesunie
                        self.logic_engine.check_player_collisions(dx=-1)
                        # self.player.move(dx=-1)
                    if event.key == pg.K_RIGHT:
                        self.logic_engine.check_player_collisions(dx=1)
                        # self.player.move(dx=1)
                    if event.key == pg.K_UP:
                        self.logic_engine.check_player_collisions(dy=-1)
                        # self.player.move(dy=-1)
                    if event.key == pg.K_DOWN:
                        self.logic_engine.check_player_collisions(dy=1)
                        # self.player.move(dy=1)
                if not self.player.pausemove:
                    if event.key == pg.K_1:
                         self.logic_engine.choose.stalowy()
                    if event.key == pg.K_2:
                        self.logic_engine.choose.silver()
                    if event.key == pg.K_3:
                        self.logic_engine.choose.axe()
                    if event.key == pg.K_4:
                        self.logic_engine.choose.bow()
                    if event.key == pg.K_5:
                        self.logic_engine.choose.fireball()
                    if event.key == pg.K_6:
                        self.logic_engine.choose.mixture()
                    if event.key == pg.K_7:
                        print("TU BĘDZIE DRZEWKO DECYZYJNE")
                self.dynamic_map = self.dynamic_map_update()
                self.inteface.draw_legend(self.dynamic_map)
            if event.type == pg.VIDEORESIZE:
                self.__resize_window__(event)

    def __resize_window__(self, event):
        """
        this handles resizing of a window, is called by events loop
        :param event, handled VIDEORESIZE pygame event"""
        #TODO ładne odświeżanie ekranu po rozszerzeniu powiększeniu
        WIDTH = event.w
        HEIGHT = event.h
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE);
