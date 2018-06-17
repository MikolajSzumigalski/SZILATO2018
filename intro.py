import pygame as pg
import sys
import os
from settings import *
from game import *
from os import *
import random
from time import sleep


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
music_folder = os.path.join(game_folder, "music")
font_name = pg.font.match_font('timesnewroman')

def draw_text(surf, text, size, x, y, bgcolor):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE, bgcolor)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Drop(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.len = random.randint(10,25)
        self.image = pg.Surface((2, self.len))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,WIDTH)
        self.rect.y = random.randint(-200,HEIGHT)
        self.yspeed = random.randint(5,10)

    def update(self):
        self.yspeed += 0.1
        self.rect.y += self.yspeed
        if(self.rect.y > HEIGHT):
            self.rect.y = random.randint(-200,-100)
            self.yspeed =  random.randint(5,10)

class Intro:
    def __init__(self, screen):
        self.screen = screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.action = None
        self.submenu = False
        self.submenu_type = None
        #init music
        pg.mixer.init()
        bg_music = pg.mixer.music.load(path.join(music_folder, 'menu.mp3'))
        self.drops = []
        for i in range(0, 500):
            self.drops.append(Drop())

        self.all_sprites = pg.sprite.Group()

        self.all_sprites.add(self.drops)

    def run(self):
        self.playing = True
        # game loop - set self.playing = False to end the game
        pg.mixer.music.play(loops = -1)
        while self.playing:
            if self.submenu: self.draw_submenu_nn()
            else: self.draw()
            self.events()
            self.update()

        return self.mode

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def button(self, btn_y, btn_msg, action):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if(545+210 > mouse[0] > 545 and btn_y + 60 > mouse[1] > btn_y):
            pg.draw.rect(self.screen, WHITE,(545,btn_y,210,60))
            pg.draw.rect(self.screen, DARKGREY,(550,btn_y+5,200,50))
            draw_text(self.screen,  btn_msg, 20, 650, btn_y+13, DARKGREY)
            if(click[0] == 1 and action != None):
                if (action == "quit"):
                    pg.quit()
                    quit()
                elif action == 'back':
                    self.submenu = False
                    self.submenu_type = None
                    sleep(0.2)
                elif action == 'neural-networks-submenu':
                    self.submenu = True
                    self.submenu_type = "neural-networks"
                    sleep(0.2)
                else:
                    self.mode = action
                    self.playing = False
        else:
            pg.draw.rect(self.screen, WHITE,(545,btn_y,210,60))
            pg.draw.rect(self.screen, BLACK,(550,btn_y+5,200,50))
            draw_text(self.screen,  btn_msg, 20, 650, btn_y+13, BLACK)

    def draw(self):
        self.bg = pg.image.load(os.path.join(img_folder, "background.png")).convert()
        self.screen.blit(self.bg, (0,0))
        self.all_sprites.draw(self.screen)
        """
        Tutaj dodajemy nowe guziki w menu.
        #pierwszy argument to wsp. y guzika, trzeba ustawic tak by guziki się na siebie nie nakładały
        #drugi argument to napis wyświetlany na guziku
        #trzeci argument to tryb ('mode') który będzie zwrócony przez intro.run() po zakończenu głównej pętli
        """
        self.button(100, "(basic+genetic_mikbal)", "basic-genetic")
        self.button(180, "neural_network_stagol", "neural-networks-submenu")
        self.button(260, "decission_tree_mikszu", "decission-tree")
        self.button(340, "placing__genetic_grzegorz", "placing-genetic")
        self.button(420, "standard", "standard")
        pg.display.flip()

    def draw_submenu_nn(self):
        self.bg = pg.image.load(os.path.join(img_folder, "background.png")).convert()
        self.screen.blit(self.bg, (0,0))
        self.all_sprites.draw(self.screen)
        self.button(100, "run game", "neural-networks")
        self.button(180, "train network", "neural-networks-training")
        self.button(260, "back", "back")
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
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
