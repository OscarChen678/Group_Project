import pygame
import sys
import math
import random
from pygame.locals import *
from player import Player
from missile import Missile
from enemy import Enemy
class Utility:
    
    def get_dis(x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def draw_text(scrn, txt, x, y, siz, col):
        fnt = pygame.font.Font(None, siz)
        cr = int(col[0] / 2)
        cg = int(col[1] / 2)
        cb = int(col[2] / 2)
        sur = fnt.render(txt, True, (cr, cg, cb))
        x = x - sur.get_width() / 2
        y = y - sur.get_height() / 2
        scrn.blit(sur, [x + 1, y + 1])
        cr = col[0] + 128
        if cr > 255:
            cr = 255
        cg = col[1] + 128
        if cg > 255:
            cg = 255
        cb = col[2] + 128
        if cb > 255:
            cb = 255
        sur = fnt.render(txt, True, (cr, cg, cb))
        scrn.blit(sur, [x - 1, y - 1])
        sur = fnt.render(txt, True, col)
        scrn.blit(sur, [x, y])
