import pygame
import system
import math
import random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 254, 0)

idx = 0
tmr = 0
laps = 0
rec = 0
recbk = 0
se_crash = None
mycar = 0

DATA_LR = []
DATA_UD = []

CLEN = len(DATA_LR)

BOARD = 120
CMAX = BOARD*CLEN
curve = [0]*CMAX
updown = [0]*CMAX

object_left = [0]*CMAX
object_right = [0]*CMAX

CAR = 30

car_x = [0]*CAR
car_y = [0]*CAR

car_lr = [0]*CAR
car_spd = [0]*CAR

PLCAR_Y = 10

LAPS = 3
laptime = ["0'00.00"]*LAPS

def make_course():
    for i in range(CLEN):
        lr1 = DATA_LR[i]
        lr2 = DATA_LR[(i + 1)%CLEN]
        ud1 = DATA_UD[i]
        ud2 = DATA_UD[(i + 1)%CLEN]

        for j in range(BOARD):
            pos = j + BOARD*i
            curve[pos] = lr1*(BOARD - j)/BOARD + lr2*j/BOARD
            updown[pos] = ud1*(BOARD - j)/BOARD + ud2*j/BOARD

            if j == 60:

