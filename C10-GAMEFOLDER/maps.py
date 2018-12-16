import pygame as pg
import random as rd
from pygame.locals import *
from settings import *
#from sprites import *
from os import path

class Map:
    def __init__(self, game):
        self.game = game
        self.platforms = {}

    def map1(self):
        self.platforms[0] = [(i, HEIGHT - 60), #底部平台集
            ] 
        self.platforms[1] = [(700, HEIGHT * 3 / 4),
            (1930, HEIGHT - 60),
            (1150, 200),
            (975, 400)]
        
