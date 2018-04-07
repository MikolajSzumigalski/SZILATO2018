#THIS FILE IS RESPONSIBLE FOR MANAGING BIG PICTURE PROGRAM LOGIC
#e.g: start menu, starting the proper game

import visual_main
import game_logic
key_presses_list = [];  # this is a list of recent non special key inputs

def startup():
    """ this starts the entire program"""
    window = visual_main.Window(); #create the window to display the content in
    startscreen(window); #handles the startscreen logic
    start_game(window);

def startscreen(window):
    """ this handles the entirety of startscreen logic and references its display logic"""
    window.show_start_screen();


def start_game(window):
    """ this handles the logic behind starting the game""";
    game_logic.new_game(window);