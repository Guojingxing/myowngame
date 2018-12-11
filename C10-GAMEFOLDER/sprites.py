from settings import *
import pygame as pg
import random as rd
from pygame.locals import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.v = vec(0, 0)
        self.a = vec(0, 0)

    def jump(self):
        #只能在站在平台的情况下跳跃
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.v.y = -20

    def update(self):
        self.a = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.a.x = -PLAYER_ACC
        if keys[K_RIGHT] or keys[K_d]:
            self.a.x = PLAYER_ACC
        #if keys[K_UP] or keys[K_w]:
            #self.v.y = -5
        #if keys[K_DOWN] or keys[K_s]:
            #self.acc.y = PLAYER_ACC
        
        self.a.x += self.v.x * PLAYER_FRICTION  #摩擦力公式 f = kv
        self.v += self.a                    #速度公式 v = at
        self.pos += self.v + 0.5*self.a     #位移公式 x = vt + 0.5*at

        #控制玩家在画面的窗口内不出界
        if self.pos.x + self.rect.width/2 >= WIDTH:
            self.pos.x = WIDTH - self.rect.width/2
        if self.pos.x - self.rect.width/2 <= 0:
            self.pos.x = self.rect.width/2
        #if self.pos.y - self.rect.height/2 <= 0:
            #self.pos.y = self.rect.height/2
        
        
        #把位置赋值给玩家的中间底部坐标
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    