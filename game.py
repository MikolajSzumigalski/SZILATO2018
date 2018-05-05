import pygame as pg
import sys
from sprites import *
from map import *
from game_logic import *
from os import path
from interface import *
class Game:
    def __init__(self, screen):
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        #init sprites and map
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 1, 1)
        self.monsters = [Leszy(self, 5, 6), Leszy(self, 6, 6), Mglak(self, 12, 1), Mglak(self, 1, 5), Spider(self, 2, 3),
                         Spider(self, 2, 2), Spider(self, 8, 4), Mglak(self, 1, 3)];
        self.map = Map(self)
        self.map.load_from_file("test.map")
        self.map.init_tile_objects()
        self.inteface = Interface(self, self.player)
        self.camera = Camera(self.map.camerawidth, self.map.cameraheight)
        #init music
        pg.mixer.init()
        bg_music = pg.mixer.music.load(path.join(music_folder, 'gamebackground.mp3'))
        self.logic_engine = LogicEngine(self)

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
