import pygame
import sys
import math
import random
from pygame.locals import *
from utility import Utility
from player import Player
from missile import Missile
from enemy import Enemy
class Enemy:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.angle = 0
        self.type = 0
        self.speed = 0
        self.shield = 0
        self.count = 0
        
    
    
    def check_collision_with_player(self, player):
        w = img_enemy[self.type].get_width()
        h = img_enemy[self.type].get_height()
        r = int((w + h) / 4 + (74 + 96) / 4)
        if Utility.get_dis(self.x, self.y, player.x, player.y) < r * r:  
            if not player.muteki > 0:
                player.shield -= 20
                if self.type != EMY_BOSS:
                    self.active = False
            
            if player.muteki == 0:
                player.muteki = 30
    def move(self, scrn, player):
        if self.active:
            ang = -90 - self.angle
            png = self.type
            if self.type < EMY_BOSS:
                self.x += self.speed * math.cos(math.radians(self.angle))
                self.y += self.speed * math.sin(math.radians(self.angle))
                
                if self.x < LINE_L or self.x > LINE_R or self.y < LINE_T or self.y > LINE_B:
                    self.active = False
            else:
                if self.count == 0:
                    self.y += 2
                    if self.y >= 200:
                        self.count = 1
                elif self.count == 1:
                    self.x -= self.speed
                    if self.x < 200:
                        for j in range(10):
                            Game.set_enemy(self.x, self.y, j * 20, EMY_BULLET, 6, 0)
                        self.count = 2
                elif self.count == 2:
                    self.x += self.speed
                    if self.x > 760:
                        for j in range(10):
                            Game.set_enemy(self.x, self.y, j * 20, EMY_BULLET, 6, 0)
                        self.count = 1
                elif self.count == 3:
                    if self.x < 480:
                        self.x += self.speed
                    else:
                        self.x -= self.speed
                    if self.y > 400:
                        self.count = 4
                elif self.count == 4:
                    self.y -= self.speed
                    if self.y < 200:
                        self.count = 3
                if game.tmr % 30 == 0:
                    Game.set_enemy(self.x, self.y, random.randint(80, 100), EMY_BULLET, 6, 0)

            if 0 <= png < len(img_enemy):
                scrn.blit(pygame.transform.rotozoom(img_enemy[png], ang, 1.0),
                          [self.x - img_enemy[png].get_width() / 2, self.y - img_enemy[png].get_height() / 2])

            if self.type != EMY_BOSS and self.shield > 0 :
                self.shield -= 1
            if self.type == EMY_BOSS:
                if self.shield == 80:
                    self.speed = 2
                    
                if self.shield == 40:
                    self.speed = 4
                if self.shield == 20:
                    self.speed = 8
            for n in range(MISSILE_MAX):
                if Game.missiles[n].active and self.type != EMY_BULLET:
                    w = img_weapon.get_width()
                    h = img_weapon.get_height()
                    r = int((w + h) / 4 + (img_enemy[png].get_width() + img_enemy[png].get_height()) / 4)
                    if Utility.get_dis(Game.missiles[n].x, Game.missiles[n].y, self.x, self.y) < r * r:
                        Game.missiles[n].active = False
                        if self.type == EMY_BOSS:
                            if self.shield > 0:
                                self.shield -= 1
                                
                                Game.explo(scrn, Game.missiles[n].x, Game.missiles[n].y)
                            else:
                                self.shield = 0
                                self.count = 3
                                self.active = False
                                

                        elif self.type == 1:
                            if self.shield >= 1:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 5
                        elif self.type == 2:
                            if self.shield >= 0:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 5

                        elif self.type == 3:
                            if self.shield >= -1:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 5
            
                           
    def check_defeat(self, game):
        if self.type == EMY_BOSS and self.shield <= 0:
            game.idx = 3