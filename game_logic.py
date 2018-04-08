#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg

#metody dla całej logiki gry (kolizje, eventy w grze itp.)

class LogicEngine:
    def __init__(self, map, player, monsters):
        self.map = map
        self.player = player
        self.monsters = monsters

    def run(self):

    def check_player_collisions(self):
        for m in self.monsters:
            if self.player.x == m.x and self.player.y == m.y
                print("colision with monster!")
