import pygame as pg

font_name = pg.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Interface:
    def __init__(self, game, x, y):
        self.image = pg.draw.rectangle
