import pygame
import sys
import math
import random
from pygame.locals import *


from utility import Utility
from player import Player
from missile import Missile
from enemy import Enemy
BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)
GOLD = (255, 255, 0)



def load_image(path):
    return pygame.image.load(path)

img_galaxy = load_image("image_gl/galaxy.png")
img_sship = [
    load_image("image_gl/starship.png"),
    load_image("image_gl/starship_l.png"),
    load_image("image_gl/starship_r.png"),
    load_image("image_gl/starship_burner.png")
]
img_weapon = load_image("image_gl/bullet.png")
img_enemy = [
    load_image("image_gl/enemy0.png"),
    load_image("image_gl/enemy1.png"),
    load_image("image_gl/enemy2.png"),
    load_image("image_gl/enemy3.png"),
    load_image("image_gl/enemy4.png"),
    load_image("image_gl/enemy_boss.png")
    
]
img_explode = [
    
    load_image("image_gl/explosion1.png"),
    load_image("image_gl/explosion2.png"),
    load_image("image_gl/explosion3.png"),
    load_image("image_gl/explosion4.png"),
    load_image("image_gl/explosion5.png")
]







# Game constants
MISSILE_MAX = 200
ENEMY_MAX = 100
EMY_BULLET = 0
EMY_BOSS = 5
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040





class Game:
    missiles = [Missile() for _ in range(MISSILE_MAX)]
    enemies = [Enemy() for _ in range(ENEMY_MAX)]
    
    tmr = 0
    score = 0
    idx = 0
    warning_timer = 0
    show_warning = False
    
    def set_missile(idx, x, y, angle):
        for i in range(MISSILE_MAX):
            if not Game.missiles[i].active:
                Game.missiles[i].active = True
                Game.missiles[i].x = x
                Game.missiles[i].y = y
                Game.missiles[i].angle = angle
                return

    
    def set_enemy(x, y, angle, typ, spd, shield = 0):
        for i in range(ENEMY_MAX):
            if not Game.enemies[i].active:
                Game.enemies[i].active = True
                Game.enemies[i].x = x
                Game.enemies[i].y = y
                Game.enemies[i].angle = angle
                Game.enemies[i].type = typ
                Game.enemies[i].speed = spd
                Game.enemies[i].shield = shield
                return

    
    def explo(scrn, x, y):
        for p in img_explode:
            scrn.blit(p, [x - 48, y - 48])
    
    
                    

    def __init__(self):
        self.player = Player()
        pygame.init()
        self.screen = pygame.display.set_mode((960, 720))
        pygame.display.set_caption("STAR WARS")
        self.clock = pygame.time.Clock()

    def main(self):
        rotation_timer = 60 
        bos = 0
        while True:
            self.screen.blit(img_galaxy, [0, 0])
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.idx == 0:
                self.tmr = 0
                Utility.draw_text(self.screen, "S T A R    W A R S", 480, 240, 100, GOLD)
                Utility.draw_text(self.screen, "Press  [SPACE]   to   Start", 480, 480, 50, SILVER)
                if key[K_SPACE] == 1:
                    self.idx = 1
                    self.player.x = 480
                    self.player.y = 600
                    self.player.shield = 100
                    self.player.muteki = 0
            elif self.idx == 1:
                self.tmr += 1
                if self.tmr % 30 == 0:
                    self.set_enemy(random.randint(20, 940), 0, 90, 1, 6)
                if self.tmr % 60 == 0:
                    self.set_enemy(random.randint(20, 940), 0, random.randint(75, 105), 2, 12) 
                if self.tmr % 120 == 0:
                    self.set_enemy(random.randint(20, 940), 0, random.randint(60, 120), 3, 6)
                if self.score >= 1500 and bos != 1 :
                    self.warning_timer = 60  
                    self.show_warning = True
                    self.set_enemy(480, -200, 90, EMY_BOSS,  1, 100)
                    bos = 1
                    

                self.player.move(self.screen, key)
                if self.player.shield <= 0:
                    self.idx = 2
                for i in range(MISSILE_MAX):
                    Game.missiles[i].move(self.screen)
                for i in range(ENEMY_MAX):
                    if Game.enemies[i].active:
                        Game.enemies[i].move(self.screen, self.player)
                        Game.enemies[i].check_collision_with_player(self.player)
                        Game.enemies[i].check_defeat(self)
                if self.show_warning:
                    Utility.draw_text(self.screen, "WARNING", 480, 360, 200, RED)
                    self.warning_timer -= 1
                    if self.warning_timer <= 0:
                        self.show_warning = False


                Utility.draw_text(self.screen, f"SCORE {self.score}", 200, 30, 50, SILVER)
                Utility.draw_text(self.screen, f"SHIELD {self.player.shield}", 760, 30, 50, CYAN)
            elif self.idx == 2:
                Utility.draw_text(self.screen, "GAME OVER", 480, 300, 200, RED)
            elif self.idx == 3:
                Utility.draw_text(self.screen, "VICTORY", 480, 300, 200, GOLD) 
            pygame.display.update()
            self.clock.tick(30)





  



if __name__ == "__main__":
    game = Game()
    game.main()