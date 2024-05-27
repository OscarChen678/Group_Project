import pygame
import sys
import math
import random
from pygame.locals import *

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 254, 0)

# Game settings
BOARD = 120
LAPS = 3
CAR = 30
PLCAR_Y = 10

# Initialization
idx = 0
tmr = 0
laps = 0
rec = 0
recbk = 0
mycar = 0

DATA_LR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
DATA_UD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CLEN = len(DATA_LR)
CMAX = BOARD * CLEN

curve = [0] * CMAX
updown = [0] * CMAX
object_left = [0] * CMAX
object_right = [0] * CMAX

car_x = [0] * CAR
car_y = [0] * CAR
car_lr = [0] * CAR
car_spd = [0] * CAR

laptime = ["0'00.00"] * LAPS


def make_course():
    for i in range(CLEN):
        lr1 = DATA_LR[i]
        lr2 = DATA_LR[(i + 1) % CLEN]
        ud1 = DATA_UD[i]
        ud2 = DATA_UD[(i + 1) % CLEN]

        for j in range(BOARD):
            pos = j + BOARD * i
            curve[pos] = lr1 * (BOARD - j) / BOARD + lr2 * j / BOARD
            updown[pos] = ud1 * (BOARD - j) / BOARD + ud2 * j / BOARD

            if j == 60:
                object_right[pos] = 1
            if i % 8 < 7:
                if j % 12 == 0:
                    object_left[pos] = 2
                elif j % 20 == 0:
                    object_left[pos] = 3
                if j % 12 == 6:
                    object_left[pos] = 9


def time_str(val):
    sec = int(val)
    ms = int((val - sec) * 100)
    mi = int(sec / 60)
    return "{}'{:02}.{:02}".format(mi, sec % 60, ms)


def draw_obj(bg, img, x, y, sc):
    img_rz = pygame.transform.rotozoom(img, 0, sc)
    w = img_rz.get_width()
    h = img_rz.get_height()
    bg.blit(img_rz, [x - w / 2, y - h])


def draw_shadow(bg, x, y, siz):
    shadow = pygame.Surface([siz, siz / 4])
    shadow.fill(RED)
    shadow.set_colorkey(RED)
    shadow.set_alpha(128)
    pygame.draw.ellipse(shadow, BLACK, [0, 0, siz, siz / 4])
    bg.blit(shadow, [x - siz / 2, y - siz / 4])


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
    if key[K_LEFT]:
        if car_lr[0] > -3:
            car_lr[0] -= 1
        car_x[0] += (car_lr[0] - 3) * car_spd[0] / 100 - 5
    elif key[K_RIGHT]:
        if car_lr[0] < 3:
            car_lr[0] += 1
        car_x[0] += (car_lr[0] + 3) * car_spd[0] / 100 + 5
    else:
        car_lr[0] = int(car_lr[0] * 0.9)

    if key[K_a]:
        car_spd[0] += 3
    elif key[K_z]:
        car_spd[0] -= 10
    else:
        car_spd[0] -= 0.25

    if car_spd[0] < 0:
        car_spd[0] = 0
    if car_spd[0] > 320:
        car_spd[0] = 320

    car_x[0] -= car_spd[0] * curve[int(car_y[0] + PLCAR_Y) % CMAX] / 50

    if car_x[0] < 0:
        car_x[0] = 0
        car_spd[0] *= 0.9
    if car_x[0] > 800:
        car_x[0] = 800
        car_spd[0] *= 0.9

    car_y[0] += car_spd[0] / 100
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
        if car_spd[i] < 100:
            car_spd[i] += 3
        if i == tmr % 120:
            car_lr[i] += random.choice([-1, 0, 1])
            if car_lr[i] < -3: car_lr[i] = -3
            if car_lr[i] > 3: car_lr[i] = 3
        car_x[i] += car_lr[i] * car_spd[i] / 100

        if car_x[i] < 50:
            car_x[i] = 50
            car_lr[i] = int(car_lr[i] * 0.9)
        if car_x[i] > 750:
            car_x[i] = 750
            car_lr[i] = int(car_lr[i] * 0.9)

        car_y[i] += car_spd[i] / 100
        if car_y[i] > CMAX - 1: car_y[i] -= CMAX

        if idx == 2:
            cx = car_x[i] - car_x[0]
            cy = car_y[i] - (car_y[0] + PLCAR_Y) % CMAX

            if -100 <= cx <= 100 and -10 <= cy <= 10:
                car_x[0] -= cx / 4
                car_x[i] += cx / 4
                car_spd[0], car_spd[i] = car_spd[i] * 0.3, car_spd[0] * 0.3


def draw_text(screen, txt, x, y, col, fnt):
    sur = fnt.render(txt, True, BLACK)
    x -= sur.get_width() / 2
    y -= sur.get_height() / 2

    screen.blit(sur, [x + 2, y + 2])
    sur = fnt.render(txt, True, col)
    screen.blit(sur, [x, y])


def draw_objects(screen, car_img, obj_img, car_speeds, car_positions, car_lr, car_spd, car_x, car_y, curve, CMAX):
    for i in range(len(car_positions)):
        x = car_x[i]
        y = car_y[i]
        lr = car_lr[i]
        spd = car_spd[i]

        y = y % CMAX
        py = (y - car_y[0]) % CMAX
        sx = car_x[0] - x
        px = sx * 800 / (800 - py)
        draw_obj(screen, car_img[mycar], 400 - px, 600 - (py / 2), 1.0)

        for j in range(10):
            idx = (int(car_y[0]) + 10 - j) % CMAX
            if object_left[idx] > 0:
                draw_obj(screen, obj_img[object_left[idx]], 50 - px / 5, 600 - (py / 2), 0.5)
            if object_right[idx] > 0:
                draw_obj(screen, obj_img[object_right[idx]], 750 - px / 5, 600 - (py / 2), 0.5)


def main():
    global idx, tmr, laps, rec, recbk, mycar

    pygame.init()
    pygame.display.set_caption("Pygame Racing Game")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    fnt_s = pygame.font.Font(None, 40)
    fnt_m = pygame.font.Font(None, 50)
    fnt_l = pygame.font.Font(None, 80)

    img_bg = pygame.image.load('img/bg.png').convert()
    #img_sea = pygame.image.load('img/sea.png').convert_alpha()
    #img_cloud = pygame.image.load('img/cloud.png').convert_alpha()
    '''img_obj = [
        None,
        pygame.image.load('img/cone.png').convert_alpha(),
        pygame.image.load('img/flag.png').convert_alpha(),
        pygame.image.load('img/obj_tree.png').convert_alpha(),
        pygame.image.load('img/obj_rock.png').convert_alpha(),
        pygame.image.load('img/obj_sign.png').convert_alpha(),
        pygame.image.load('img/obj_windmill.png').convert_alpha(),
        pygame.image.load('img/obj_billboard.png').convert_alpha(),
        pygame.image.load('img/obj_barn.png').convert_alpha(),
        pygame.image.load('img/obj_saku.png').convert_alpha()
    ]'''

    img_car = [
        pygame.image.load('img/car0.png').convert_alpha(),
        pygame.image.load('img/car1.png').convert_alpha(),
        pygame.image.load('img/car2.png').convert_alpha(),
        pygame.image.load('img/car3.png').convert_alpha(),
        pygame.image.load('img/car4.png').convert_alpha(),
        pygame.image.load('img/car5.png').convert_alpha()
    ]

    make_course()
    init_car()

    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        # Updating game state
        if idx == 0:
            if key[K_SPACE]:
                idx = 1
                tmr = 0
                laps = 0
                rec = 0
                recbk = 0
                init_car()

        elif idx == 1:
            if tmr == 60:
                idx = 2
                tmr = 0

        elif idx == 2:
            rec += 1 / 60
            drive_car(key)
            move_car(1)
            if tmr % 10 == 0:
                move_car(0)

        elif idx == 3:
            if tmr == 300:
                idx = 0
                tmr = 0

        # Drawing
        screen.blit(img_bg, [0, 0])

        sc_y = (tmr * 10) % 800
        #screen.blit(img_sea, [0, sc_y - 800])
        #screen.blit(img_sea, [0, sc_y])

        if idx == 0:
            draw_text(screen, "PRESS SPACE KEY", 400, 300, RED, fnt_l)
        elif idx == 1:
            if 1 <= tmr <= 4:
                draw_text(screen, str(4 - tmr), 400, 300, YELLOW, fnt_l)
        elif idx == 2 or idx == 3:
            # Drawing cars, objects, and other elements
            draw_objects(screen, img_car, img_obj, car_spd, car_y, car_lr, car_spd, car_x, car_y, curve, CMAX)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
