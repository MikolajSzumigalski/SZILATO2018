#THIS FILE IS RESPONSIBLE FOR PROPER IN GAME LOGIC
import pygame as pg

#metody dla całej logiki gry (kolizje, eventy w grze itp.)

class LogicEngine:
    def __init__(self, map, player, monsters):
        self.map = map
        self.player = player
        self.monsters = monsters

    
