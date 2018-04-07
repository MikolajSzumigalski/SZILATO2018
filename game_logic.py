#this file runs the in-game logic
import visual_main
import pygame as pg
import program_logic
def new_game(window):
    """
    prepares the starting in-game logic
    :param window: Window object from visual_main, main visual window to display on
    :return:
    """
    #TODO WSZYSTKO
    player_starting_location = (10,10)
    monsters_list = [];
    # monsters_list = [{'type': "Snake", 'x':2, 'y':2}];

    window.new(monsters_list, player_starting_location[0], player_starting_location[1]); #nowy stan początkowy

    walking(window);

def walking(window):
    """
    this function is responsible for in game logic walking and calls to visual_main
    """
    while True: #nie kolizja albo coś, czary mary game logika #TODO
        key = input_loop(window);
        if key == pg.K_LEFT:
            window.player.move(dx=-1)
        if key == pg.K_RIGHT:
            window.player.move(dx=1)
        if key == pg.K_UP:
            window.player.move(dy=-1)
        if key == pg.K_DOWN:
            window.player.move(dy=1)

def input_loop(window):
    """
    this function runs the game until an input is received
    :param window: Window object from visual_main, that receives input presses
    :return: key pressed in an int (pygame) representation
    """
    program_logic.key_presses_list.clear();
    window.run();
    return program_logic.key_presses_list.pop()




