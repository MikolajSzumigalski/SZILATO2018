#THIS FILE IS RESPONSIBLE FOR MANAGING BIG PICTURE PROGRAM LOGIC
#e.g: start menu, starting the proper game

import visual_main
import game_logic
key_presses_list = [];  # this is a list of recent non special key inputs

def startup():
    """ this starts the entire program"""
    window = visual_main.Window(); #create the window to display the content in


    #tworzymy okno
    #wyświetlamy menu
    #startujemy grę
