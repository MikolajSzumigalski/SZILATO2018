import pygame as pg
from settings import *
import copy
pg.font.init()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
font_name = pg.font.match_font('timesnewroman')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_hp(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    while(len(text)<5):
        text = text + " "
    text_surface = font.render(text, True, WHITE, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Interface:
    def __init__(self, game, player):
        self.width = 300
        self.height = 500
        self.game = game
        self.surface = pg.Surface((200, 500))
        self.surface.fill(BLACK)
        self.image = pg.Surface((80, 64))
        self.image = pg.image.load(os.path.join(img_folder, "wolf.png")).convert()
        self.image = pg.transform.scale(self.image, (80, 64))
        self.image.set_colorkey(BLACK)
        self.surface.blit(self.image, (50,0))
        #WYSWIETLANIE HP
        self.image = pg.Surface((32, 32))
        self.image = pg.image.load(os.path.join(img_folder, "serce.png")).convert()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)
        self.surface.blit(self.image, (0,65))
        draw_hp(self.surface, str(player.hp), 25, 65, 65)
        #WYŚWIETLANIE POZIOMU
        draw_text(self.surface, "LEVEL: ", 20, 40, 95)
        draw_text(self.surface,  str(player.lev), 20, 90, 95)
        #WYŚWIETLANIE EXPA
        draw_text(self.surface, "EXP: ", 20, 32, 130)
        draw_text(self.surface,  str(player.total_exp) + " / " + str(sum([100 * level for level in range(1, player.lev+1)])), 20, 100, 130)
        #WYŚWIETLANIE ATAKU
        draw_text(self.surface,  "ATK: ", 20, 32, 150)
        draw_text(self.surface,  str(player.get_total_at()), 20, 120, 150)
        #WYŚWIETLNIE OBRONY
        draw_text(self.surface,  "DEF: ", 20, 32, 170)
        draw_text(self.surface,  str(player.get_total_deff()), 20, 120, 170)
        #WYSWIETLANIE LEGENDY POTWORÓW
        self.image = pg.Surface((32, 32))
        #self.image = pg.image.load(os.path.join(img_folder, "monsters.png")).convert()
        #self.image = pg.transform.scale(self.image, (201, 239))
        #self.image.set_colorkey(BLACK)
        #self.surface.blit(self.image, (0,260))
        #LEGENDA MAPY
        self.legend_size_x = 201 // GRIDWIDTH
        self.legend_size_y = 239 // GRIDHEIGHT
        self.legend_size = min(self.legend_size_x, self.legend_size_y)
        self.border = pg.Surface((201,239))
        self.border.fill((30,30,30))
        self.image = pg.Surface((199, 237))
        self.image.fill((0,0,0))

    def draw_legend(self, map):
        for i in range (0, len(map)):
            for j in range(0, len(map[i])):
                if map[i][j] == 0:
                    color = (255, 255, 255)
                elif map[i][j] == 1:
                    color = (0, 0, 0)
                elif map[i][j] == 2:
                     color = (255, 0, 0)
                elif map[i][j] == 3:
                     color = (0, 0, 255)
                else:
                    color = (255, 0, 255)
                pg.draw.rect(self.image, color, ( j*self.legend_size+1,i*self.legend_size+1, self.legend_size-1, self.legend_size-1))
        self.surface.blit(self.image, (0,260))


    def draw_interface(self, screen):
        screen.blit(self.surface, (600, 0))

    def update(self, player):
        draw_hp(self.surface, str(player.hp), 25, 65, 65)
        draw_text(self.surface,  str(player.lev), 20, 90, 95)
        draw_text(self.surface,  str(player.total_exp) + " / " + str(sum([100 * level for level in range(1, player.lev+1)])), 20, 100, 130)
        draw_text(self.surface,  str(player.get_total_at()), 20, 120, 150)
        draw_text(self.surface,  str(player.get_total_deff()), 20, 120, 170)
