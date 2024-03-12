import pygame
import sys
import math
from pygame.locals import *

board = 120
cmax = board*4
curve = [0]*cmax

def make_course():
    for i in range(360):
        curve[board + i] = int (5*math.sin(math.radians(i)))

def main():
    pygame.init()
    pygame.display.set_caption("back_ground")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    #img_bg = pygame.image.load("img/bg.png").convert()

    board_w = [0]*board
    board_h = [0]*board
    for i in range(board):
        board_w[i] = 10 + (board - i)*(board - i)/12
        board_h[i] = 3.4*(board - i)/board

    make_course()

    car_y = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        if key[K_UP] == 1:
            car_y = (car_y + 1)%cmax

        di = 0
        board_x = [0]*board
        for i in range(board):
            di += curve[(car_y + i)%cmax]
            board_x[i] = 400 - board_w[i]/2 + di/2

        sy = 400

        #screen.blit(img_bg, [0, 0])
        screen.fill((0, 100, 0))


        for i in range(board - 1, 0, -1):
            ux = board_x[i]
            uy = sy
            uw = board_w[i]
            sy = sy + board_h[i]

            bx = board_x[i-1]
            by = sy
            bw = board_w[i-1]

            col = (160, 160, 160)
            if (car_y + i)%12 == 0:
                col = (255, 255, 255)

            pygame.draw.polygon(screen, col, [[ux, uy], [ux + uw, uy], [bx + bw, by], [bx, by]])

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()

