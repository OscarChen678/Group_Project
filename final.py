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
                object_right[pos] = 1
            if i%8 < 7:
                if j%12 == 0:
                    object_left[pos] = 2
                else:
                    if j%20 == 0:
                        object_left[pos] = 3
                if j%12 == 6:
                    object_left[pos] = 9
def time_str(val):
    sec = int(val)
    ms = int((val - sec) * 100)
    mi = int(sec/60)
    return "{}'{:02}.{:02}".format(mi, sec%60, ms)

def draw_obj(bg, img, x, y, sc):
    img_rz = pygame.transform.rotozoom(img, 0, sc)
    w = img_rz.get_width()
    h = img_rz.get_height()
    bg.blit(img_rz, [x - w/2, y - h])

def draw_shadow(bg, x, y, siz):
    shadow = pygame.Surface([siz, siz/4])
    shadow.fill(RED)
    shadow.set_colorkey(RED)
    shadow.set_alpha(128)
    pygame.draw.ellipse(shadow, BLACK, [0, 0, siz, siz/4])
    bg.blit(shadow, [x - siz/2, y - siz/4])

def init_car():
    for i in range(1, CAR):
        car_x[i] = random.randint(50, 750)
        car_y[i] = random.randint(200, CMAX - 200)
        car_lr[i] = 0
        car_spd[i] = random.randint(100, 200)

    car_x[0] = 400
    car_y[0] = 0
    car_lr[0] = 0
    car_spd[0] = 0

def drive_car(key):
    global idx, tmr, laps, recbk
    if key[K_LEFT] == 1:
        if car_lr[0] > -3:
            car_lr[0] -= 1
        car_x[0] = car_x[0] + (car_lr[0] - 3)*car_spd[0]/100 - 5
    elif key[K_RIGHT] == 1:
        if car_lr[0] < 3:
            car_lr[0] += 1
        car_x[0] = car_x[0] + (car_lr[0] + 3)*car_spd[0]/100 + 5

    else:
        car_lr[0] = int(car_lr[0]*0.9)

    if key[K_a] == 1:
        car_spd[0] += 3
    elif key[K_z] == 1:
        car_spd[0] -= 10
    else:
        car_spd[0] -= 0.25

    if car_spd[0] < 0:
        car_spd[0] = 0
    if car_spd[0] > 320:
        car_spd[0] = 320

    car_x[0] -= car_spd[0]*curve[int(car_y[0]+PLCAR_Y)%CMAX]/50

    if car_x[0] < 0:
        car_x[0] = 0
        car_spd[0] *= 0.9
    if car_x[0] > 800:
        car_x[0] = 800
        car_spd[0] *= 0.9

    car_y[0] = car_y[0] + car_spd[0]/100
    if car_y[0] > CMAX - 1:
        car_y[0] -= CMAX
        laptime[laps] = time_str(rec - recbk)
        recbk = rec
        laps += 1
        if laps == LAPS:
            idx = 3
            tmr = 0


def move_car(cs):
    for i in range(cs, CAR):
        if car_spd[i] <　100:
            car_spd[i] += 3
        if i == tmr%120:
            car_lr[i] += random.choice([-1, 0, 1])
            if car_lr[i] < -3: car_lr[i] = -3
            if car_lr[i] > 3: car_lr[i] = 3
        car_x[i] = car_x[i] + car_lr[i]*car_spd[i]/100

        if car_x[i] < 50:
            car_x[i] = 50
            car_lr[i] = int(car_lr[i]*0.9)
        if car_x[i] > 750:
            car_x[i] = 750
            car_lr[i] = int(car_lr[i]*0.9)

        car_y[i] += car_spd[i]/100
        if car_y[i] > CMAX - 1: car_y[i] -= CMAX
        if idx == 2:
            cx = car_x[i] - car_x[0]
            cy = car_y[i] - (car_y[0] + PLCAR_Y)%CMAX

            if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10:
                car_x[0] -= cx/4
                car_x[i] += cx/4
                car_spd[0], car_spd[i] = car_spd[i]*0.3, car_spd[0]*0.3


def draw_text(scrn, txt, x, y, col, fnt):
    sur = fnt.render(txt, True, BLACK)
    x -= sur.get_width()/2
    y -= sur.get_height()/2

    scrn.blit(sur, [x + 2, y + 2])
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, [x, y])


def main():
    global idx, tmr, laps, rec, recbk, mycar

    pygame.init()
    pygame.display.set_caption('racer')
    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()
    fnt_s = pygame.font.Font(None, 40)
    fnt_m = pygame.font.Font(None, 50)
    fnt_l = pygame.font.Font(None, 120)

    img_title = pygame.image.load('image_pr/title.png').convert_alpha()
    img_bg = pygame.image.load('image_pr/bg.png').convert_alpha()
    img_sea = pygame.image.load('image_pr/sea.png').convert_alpha()
    img_obj = [None, ]
    img_car = []

    BOARD_W = [0]*BOARD
    BOARD_H = [0]*BOARD
    BOARD_UD = [0]*BOARD
    for i in range(BOARD):
        BOARD_W[i] = 10 + (BOARD - i)*(BOARD - i)/12
        BOARD_H[i] = 3.4*(BOARD - i)/BOARD
        BOARD_UD[i] = 2*matt.sin(math.radians(i*1.5))

    make_course()
    init_car()

    vertical = 0


