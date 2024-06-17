import pygame
import sys
import math
import random
from pygame.locals import *
import chart as ch

from utility import Utility

BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)
GOLD = (255, 255, 0)
PINK = (255, 0, 255)
kd = [0, 0, 0]
mi = [0, 0]


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
    load_image("image_gl/enemy_boss.png"),
    load_image("image_gl/enemy_boss.png")
]
img_explode = [
    load_image("image_gl/explosion1.png"),
    load_image("image_gl/explosion2.png"),
    load_image("image_gl/explosion3.png"),
    load_image("image_gl/explosion4.png"),
    load_image("image_gl/explosion5.png")
]


###############################################
MISSILE_MAX = 200
ENEMY_MAX = 100
EMY_BULLET = 0
EMY_BOSS = 5
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040



class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.shield = 0
        self.muteki = 0
        self.key_spc = 0
        self.key_z = 0

    def move(self, scrn, key):
        self.direction = 0
        if key[K_UP] == 1:
            self.y -= 20
            if self.y < 80:
                self.y = 80
        if key[K_DOWN] == 1:
            self.y += 20
            if self.y > 640:
                self.y = 640
        if key[K_LEFT] == 1:
            self.direction = 1
            self.x -= 20
            if self.x < 40:
                self.x = 40
        if key[K_RIGHT] == 1:
            self.direction = 2
            self.x += 20
            if self.x > 920:
                self.x = 920
        self.key_spc = (self.key_spc + 1) * key[K_SPACE]
        if self.key_spc % 5 == 1 and self.muteki == 0:
            Game.set_missile(0, self.x, self.y, 270) 
            mi[0] += 1
        self.key_z = (self.key_z + 1) * key[K_z]
        if self.key_z == 1:
            if self.shield > 30:
                self.shield -= 30 

                for angle in range(0, 360, 15):
                    Game.set_missile(0, self.x, self.y, angle)
                    mi[0] += 1

        if self.muteki % 2 == 0:
            scrn.blit(img_sship[3], [self.x - 8, self.y + 40 + (Game.tmr % 3) * 2])
            scrn.blit(img_sship[self.direction], [self.x - 37, self.y - 48])
        if self.muteki > 0:
            self.muteki -= 1

class Missile:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.angle = 0
    def move(self, scrn):
        if self.active:
            self.x += 36 * math.cos(math.radians(self.angle))
            self.y += 36 * math.sin(math.radians(self.angle))
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - self.angle, 1.0)
            scrn.blit(img_rz, [self.x - img_rz.get_width() / 2, self.y - img_rz.get_height() / 2])
            if self.y < 0 or self.x < 0 or self.x > 960 or self.y > 720:
                self.active = False


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
                player.muteki = 60
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
                global hp
                hp = self.shield
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
            if self.type == EMY_BOSS:
                if self.shield == 80:
                    self.speed = 2
                if self.shield == 60:
                    self.speed = 4
                if self.shield == 40:
                    self.speed = 10
            for n in range(MISSILE_MAX):
                if Game.missiles[n].active and self.type != EMY_BULLET:
                    w = img_weapon.get_width()
                    h = img_weapon.get_height()
                    r = int((w + h) / 4 + (img_enemy[png].get_width() + img_enemy[png].get_height()) / 4)
                    if Utility.get_dis(Game.missiles[n].x, Game.missiles[n].y, self.x, self.y) < r * r:
                        Game.missiles[n].active = False
                        mi[1] += 1
                        if self.type == EMY_BOSS:
                            if self.shield > 0:
                                self.shield -= 1
                                hp = self.shield
                                
                                Game.explo(scrn, Game.missiles[n].x, Game.missiles[n].y)
                            else:
                                hp = 0
                                self.shield = 0
                                self.count = 3
                                self.active = False
                                

                        elif self.type == 1:
                            if self.shield > 0:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 5
                                kd[0] += 1
                        elif self.type == 2:
                            if self.shield > 0:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 10
                                kd[1] += 1

                        elif self.type == 3:
                            if self.shield > 0:
                                self.shield -= 1
                            else:
                                self.active = False
                                Game.explo(scrn, self.x, self.y)
                                Game.score += 100
                                player.shield += 15
                                kd[2] += 1
            
            
                           
    def check_defeat(self, game):
        if self.type == EMY_BOSS and self.shield <= 0:
            game.idx = 3

class Game:
    missiles = [Missile() for _ in range(MISSILE_MAX)]
    enemies = [Enemy() for _ in range(ENEMY_MAX)]
    tmr = 0
    score = 0
    idx = 0
    warning_timer = 0
    show_warning = False
    @staticmethod
    def set_missile(idx, x, y, angle):
        for i in range(MISSILE_MAX):
            if not Game.missiles[i].active:
                Game.missiles[i].active = True
                Game.missiles[i].x = x
                Game.missiles[i].y = y
                Game.missiles[i].angle = angle
                return
    @staticmethod
    def set_enemy(x, y, angle, typ, spd, shield):
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

    @staticmethod
    def explo(scrn, x, y):
        for p in img_explode:
            scrn.blit(p, [x - 48, y - 48])
    
    
    def __init__(self):
        self.player = Player()
        pygame.init()
        self.screen = pygame.display.set_mode((960, 720))
        pygame.display.set_caption("GALAXY WARS")
        self.clock = pygame.time.Clock()

    def main(self):
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
                Utility.draw_text(self.screen, "G A L A X Y    W A R S", 480, 240, 100, GOLD )
                Utility.draw_text(self.screen, "Press [SPACE] to Start", 480, 480, 50, SILVER)
                if key[K_SPACE] == 1:
                    self.idx = 1
                    self.player.x = 480
                    self.player.y = 600
                    self.player.shield = 100
                    self.player.muteki = 0
            elif self.idx == 1:
                self.tmr += 1
                if self.tmr % 30 == 0:
                    self.set_enemy(random.randint(20, 940), 0, 90, 1, 6, 0)
                if self.tmr % 60 == 0:
                    self.set_enemy(random.randint(20, 940), 0, random.randint(75, 105), 2, 12, 1) 
                if self.tmr % 120 == 0:
                    self.set_enemy(random.randint(20, 940), 0, random.randint(60, 120), 3, 6, 2)
                if self.score >= 1500 and bos != 1 :
                    self.warning_timer = 60  
                    self.show_warning = True
                    self.set_enemy(480, -200, 90, EMY_BOSS,  1, 100)
                    bos = 1
                    

                self.player.move(self.screen, key)
                if self.player.shield <= 0:
                    self.player.shield = 0
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
                
                if bos == 1:
                    Utility.draw_text(self.screen, f"BOSS HP {hp}", 760, 80, 50, PINK)
                Utility.draw_text(self.screen, f"SCORE {self.score}", 200, 30, 50, SILVER)
                Utility.draw_text(self.screen, f"SHIELD {self.player.shield}", 760, 30, 50, CYAN)
            elif self.idx == 2:
                Utility.draw_text(self.screen, "GAME OVER", 480, 300, 200, RED)

                if key[K_f] == 1:
                    ch.create_dual_pie_charts(kd, mi)
                    
            elif self.idx == 3:
                Utility.draw_text(self.screen, "VICTORY", 480, 300, 200, GOLD) 
                if key[K_f] == 1:
                    ch.create_dual_pie_charts(kd, mi)
            pygame.display.update()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.main()

