import pygame as pg
import sys
from settings import *
from sprites import *
import program_logic;

#THIS FILE HANDLES PYGAME REPRESENTATION OF PROGRAM AND IN-GAME LOGIC
class Window:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)


    def new(self, monster_list, player_location_x=10, player_location_y=10):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, player_location_x, player_location_y)
        self.monsters = [Snake(self, 5, 6)];
        for x in range(10, 20):
            Wall(self, x, 5)

    def run(self):
        # game loop
        waskeypressed = False;
        while not waskeypressed:
            self.dt = self.clock.tick(FPS) / 1000
            waskeypressed = self.events();
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()



    def events(self):
        """
        handles big scope window input (resizing). Takes in  all button presses events
        and returns the type of button pressed in pygame representation
        appends the keydown to a list of key_presses_list from program_logic
        :return Returns True if a nonspecial key was pressed
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                program_logic.key_presses_list.append(event.key);
                return True
            if event.type == pg.VIDEORESIZE:
                self.__resize_window__(event);

            return False


    def __resize_window__(self, event):
        """
        this handles resizing of a window, is called by events loop
        :param event, handled VIDEORESIZE pygame event"""
        #TODO ładne odświeżanie ekranu po rozszerzeniu powiększeniu
        WIDTH = event.w
        HEIGHT = event.h
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE);

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


if __name__ == "__main__":
    # create the game window
    g = Window()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
    g.show_go_screen()
