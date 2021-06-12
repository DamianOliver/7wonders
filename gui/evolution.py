import pygame as pg
from random import *

pg.init()

screen_dimension = (2500, 1385)
screen = pg.display.set_mode(screen_dimension, pg.RESIZABLE)

class Species:
    def init(location, speed):
        self.speed = speed
        self.location = location

    def choose_action(self):

    
