import pygame
import sys
import math
import random
from pygame.locals import *
from utility import Utility
from player import Player
from missile import Missile
from enemy import Enemy
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.shield = 0
        self.muteki = 0
        self.key_spc = 0
        self.key_z = 0

    def move(self, scrn, key):
        self.direction = 0
        if key[K_UP] == 1:
            self.y -= 20
            if self.y < 80:
                self.y = 80
        if key[K_DOWN] == 1:
            self.y += 20
            if self.y > 640:
                self.y = 640
        if key[K_LEFT] == 1:
            self.direction = 1
            self.x -= 20
            if self.x < 40:
                self.x = 40
        if key[K_RIGHT] == 1:
            self.direction = 2
            self.x += 20
            if self.x > 920:
                self.x = 920
        self.key_spc = (self.key_spc + 1) * key[K_SPACE]
        if self.key_spc % 5 == 1 and self.muteki == 0:
            Game.set_missile(0, self.x, self.y, 270)  # Default angle for straight shooting
        self.key_z = (self.key_z + 1) * key[K_z]
        if self.key_z == 1:
            if self.shield > 30:
                self.shield -= 30 

                for angle in range(0, 360, 15):  # Change the step to adjust the number of missiles
                    Game.set_missile(0, self.x, self.y, angle)

        if self.muteki % 2 == 0:
            scrn.blit(img_sship[3], [self.x - 8, self.y + 40 + (Game.tmr % 3) * 2])
            scrn.blit(img_sship[self.direction], [self.x - 37, self.y - 48])
        if self.muteki > 0:
            self.muteki -= 1
        
