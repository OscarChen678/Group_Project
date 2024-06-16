import pygame
import sys
import math
import random
from pygame.locals import *
from utility import Utility
from player import Player
from enemy import Enemy
class Missile:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.angle = 0

    def move(self, scrn):
        if self.active:
            self.x += 36 * math.cos(math.radians(self.angle))
            self.y += 36 * math.sin(math.radians(self.angle))
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - self.angle, 1.0)
            scrn.blit(img_rz, [self.x - img_rz.get_width() / 2, self.y - img_rz.get_height() / 2])
            if self.y < 0 or self.x < 0 or self.x > 960 or self.y > 720:
                self.active = False