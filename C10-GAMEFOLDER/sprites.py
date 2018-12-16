import pygame as pg
from pygame.locals import *
import random as rd
from settings import *
from maps import *
vec = pg.math.Vector2

class Spritesheet:
    # 加载各种sprite
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        #self.lives = 5 #一共有5条命
        #加载图片
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3, HEIGHT / 2) #游戏开始时的位置
        self.pos = vec(WIDTH / 3, HEIGHT / 2)       #游戏开始时的位置
        self.vel = vec(0, 0)
        self.a = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frame_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                          self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frame_l = []
        for frame in self.walk_frame_r:
            frame.set_colorkey(BLACK)
            self.walk_frame_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -8:
                self.vel.y = -8

    def jump(self):
        #只能在站在平台的情况下跳跃
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.vel.y = -PLAYER_JUMP   #给玩家一个向上的初速度
            self.jumping = True
            self.walking = False

    def update(self):
        self.animate()
        self.a = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.a.x = -PLAYER_ACC
        if keys[K_RIGHT] or keys[K_d]:
            self.a.x = PLAYER_ACC

        self.a.x += self.vel.x * PLAYER_FRICTION	#摩擦力公式 f = kv
        self.vel += self.a	#速度公式 v = at
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.a	#位移公式 x = vt + 0.5*at
		#控制玩家在画面的窗口内不出界
        if self.pos.x + self.rect.width/2 >= WIDTH:
            self.pos.x = WIDTH - self.rect.width/2
        if self.pos.x - self.rect.width/2 <= 0:
            self.pos.x = self.rect.width/2
		#把位置赋值给玩家的中间底部坐标
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        
        #走路动画
        if self.walking:
            if now - self.last_update > 200:    #走路速度200毫秒切换一帧
                self.last_update = now
                old_bottom = self.rect.midbottom
                if self.vel.x < 0:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frame_l)
                    self.image = self.walk_frame_l[self.current_frame]
                if self.vel.x > 0:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frame_r)
                    self.image = self.walk_frame_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.midbottom = old_bottom
        #跳跃动画
        if self.jumping:
            old_bottom = self.rect.midbottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_bottom
        
        #站立动画
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                old_bottom = self.rect.midbottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.midbottom = old_bottom
        self.mask = pg.mask.from_surface(self.image)

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = rd.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = rd.randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),\
                                                     int(self.rect.height * scale)))
        self.rect.y = rd.randrange(HEIGHT - self.rect.height)
        self.rect.x = rd.randrange(WIDTH, WIDTH * 2)

    def update(self):
        if self.rect.right < 0:
            self.kill()

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [self.game.spritesheet.get_image(0, 288, 380, 94), #长
                  self.game.spritesheet.get_image(213, 1662, 201, 100), #短
                  self.game.spritesheet.get_image(0, 384, 380, 94), #裂长
                  self.game.spritesheet.get_image(382, 204, 200, 100) ] #裂短
        self.image = rd.choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if rd.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

        #if rd.randrange(100) < POW_SPAWN_PCT-3:
            #Carrot(self.game, self)
        #if rd.randrange(100) < POW_SPAWN_PCT+30:
            #Bronze(self.game, self)
        #if rd.randrange(100) < POW_SPAWN_PCT+15:
            #Silver(self.game, self)
        #if rd.randrange(100) < POW_SPAWN_PCT-5:
            #Gold(self.game, self)

class Platform2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100),
                  self.game.spritesheet.get_image(0, 384, 380, 94),
                  self.game.spritesheet.get_image(382, 204, 200, 100)]
        self.image = rd.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.x > 1280:
            if rd.randrange(10000) < POW_SPAWN_PCT:
                p = Pow2(self.game, self)
                self.game.powerups.add(p)
                self.game.all_sprites.add(p)

        if self.rect.x > 1280:
            if rd.randrange(10000) < POW_SPAWN_PCT+3:
                p = Carrot2(self.game, self)
                self.game.carrots.add(p)
                self.game.all_sprites.add(p)
        if self.rect.x > 1280:
            if rd.randrange(10000) < POW_SPAWN_PCT+30:
                p = Bronze2(self.game, self)
                self.game.bronzes.add(p)
                self.game.all_sprites.add(p)
        if self.rect.x > 1280:
            if rd.randrange(10000) < POW_SPAWN_PCT+15:
                p = Silver2(self.game, self)
                self.game.silvers.add(p)
                self.game.all_sprites.add(p)
        if self.rect.x > 1280:
            if rd.randrange(10000) < POW_SPAWN_PCT-5:
                p = Gold2(self.game, self)
                self.game.golds.add(p)
                self.game.all_sprites.add(p)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Pow2(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Carrot(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.carrots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['carrot'])
        self.image = self.game.spritesheet.get_image(820, 1733, 78, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx - 20
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Carrot2(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['carrot'])
        self.image = self.game.spritesheet.get_image(820, 1733, 78, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx - 20
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Bronze(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['bronze'])
        self.image = self.game.spritesheet.get_image(329, 1390, 60, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Bronze2(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['bronze'])
        self.image = self.game.spritesheet.get_image(329, 1390, 60, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Silver(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['silver'])
        self.image = self.game.spritesheet.get_image(307, 1981, 61, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Silver2(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['silver'])
        self.image = self.game.spritesheet.get_image(307, 1981, 61, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Gold(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['gold'])
        self.image = self.game.spritesheet.get_image(244, 1981, 61, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Gold2(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.type = rd.choice(['gold'])
        self.image = self.game.spritesheet.get_image(244, 1981, 61, 61)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = rd.choice([-100, WIDTH + 100])
        self.vx = rd.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = rd.randrange(90, 680, 180)
        self.vy = 0
        self.dy = 0.5
    
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()