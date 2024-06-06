import pygame
import sys
import math
import random
from pygame.locals import *

FIG = 30
fig_x = [0]*FIG
fig_y = [0]*FIG
fig_lr = [0]*FIG
fig_spd = [0]*FIG
PLFIG_Y = 10

def init_fig():
    for i in range(1, FIG):
        fig_x[i] = random.randint(50, 750)
        fig_y[i] = random.randint(200, CMAX-200)
        fig_lr[i] = 0
        fig_spd[i] = random.randint(100, 200)
    fig_x[0] = 400
    fig_y[0] = 0
    fig_lr[0] = 0
    fig_spd[0] = 0

def move_fig(key):
    global idx, tmr, laps, recbk
    if key[K_LEFT] == 1:
        if fig_lr[0] > -3:
            fig_lr[0] -= 1
        fig_x[0] = fig_x[0] + (fig_lr[0]-3)*fig_spd[0]/100 - 5
    elif key[K_RIGHT] == 1:
        if fig_lr[0] < 3:
            fig_lr[0] += 1
        fig_x[0] = fig_x[0] + (fig_lr[0]+3)*fig_spd[0]/100 + 5
    else:
        fig_lr[0] = int(fig_lr[0]*0.9)

    if key[K_a] == 1:
        fig_spd[0] += 3
    elif key[K_z] == 1:
        fig_spd[0] -= 10
    else:
        fig_spd[0] -= 0.25

    if fig_spd[0] < 0:
        fig_spd[0] = 0
    if fig_spd[0] > 320:
        fig_spd[0] = 320

    fig_x[0] -= fig_spd[0]*curve[int(fig_y[0]+PLCAR_Y)%CMAX]/50
    if fig_x[0] < 0:
        fig_x[0] = 0
        fig_spd[0] *= 0.9
    if fig_x[0] > 800:
        fig_x[0] = 800
        fig_spd[0] *= 0.9

    fig_y[0] = fig_y[0] + fig_spd[0]/100
    if fig_y[0] > CMAX-1:
        fig_y[0] -= CMAX
        laptime[laps] = time_str(rec-recbk)
        recbk = rec
        laps += 1
        if laps == LAPS:
            idx = 3
            tmr = 0

def move_com(cs):
    for i in range(cs, CAR):
        if fig_spd[i] < 100:
            fig_spd[i] += 3
        if i == tmr%120:
            fig_lr[i] += random.choice([-1,0,1])
            if fig_lr[i] < -3: fig_lr[i] = -3
            if fig_lr[i] >  3: fig_lr[i] =  3
        fig_x[i] = fig_x[i] + fig_lr[i]*fig_spd[i]/100
        if fig_x[i] < 50:
            fig_x[i] = 50
            fig_lr[i] = int(fig_lr[i]*0.9)
        if fig_x[i] > 750:
            fig_x[i] = 750
            fig_lr[i] = int(fig_lr[i]*0.9)
        fig_y[i] += fig_spd[i]/100
        if fig_y[i] > CMAX-1:
            fig_y[i] -= CMAX
        if idx == 2:
            cx = fig_x[i]-fig_x[0]
            cy = fig_y[i]-(fig_y[0]+PLCAR_Y)%CMAX
            if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10:
                
                fig_x[0] -= cx/4
                fig_x[i] += cx/4
                fig_spd[0], fig_spd[i] = fig_spd[i]*0.3, fig_spd[0]*0.3
                

