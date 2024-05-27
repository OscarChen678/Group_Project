import pygame
import sys
from pygame.locals import *

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Car dimensions
CAR_WIDTH = 50
CAR_HEIGHT = 80
CAR_SPEED = 5

class Car:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT

    def move_left(self):
        self.x -= CAR_SPEED

    def move_right(self):
        self.x += CAR_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Simple Racing Game')
    clock = pygame.time.Clock()

    player_car = Car()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player_car.move_left()
        if keys[K_RIGHT]:
            player_car.move_right()

        screen.fill(WHITE)
        player_car.draw(screen)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
