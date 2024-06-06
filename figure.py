import pygame
import sys
import math
import random
from pygame.locals import *

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