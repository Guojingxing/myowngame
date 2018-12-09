#pygame 游戏开发1 - 飞机大战
import os
import pygame
from pygame.locals import *
import random
from settings import *

pygame.init()
pygame.mixer.init()

s = WIDTH, HEIGHT
window = pygame.display.set_mode(s)
pygame.display.set_caption(u'我的第一个游戏')

#文件位置
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
block_folder = os.path.join(img_folder, "blocks")
space_holder = os.path.join(img_folder, "spaceshooter")
PNGS = os.path.join(space_holder, "PNG")
sound = os.path.join(game_folder, "sound")
explode_dir = os.path.join(space_holder, "Explosions")
powerup_dir = os.path.join(PNGS, "Power-ups")

clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")

#字体
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#命 - 绿条
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    pygame.draw.rect(surf, WHITE, outline_rect)
    if fill > 20:
        pygame.draw.rect(surf, GREEN, fill_rect)
    elif fill:
        pygame.draw.rect(surf, RED, fill_rect)

#初始3条命的小图标
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

count = 0
#一个敌人消亡后，产生一个新的敌人
def newmob(game_count = 0):
    game_count += 1
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    if game_count > 20:
        for i in range(game_count//10):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

#显示继续游戏屏幕，或者游戏结束屏幕
def show_go_screen():
    window.blit(background, background_rect)
    draw_text(window, "your final score: %05d"%score, int(HEIGHT / 20), WIDTH / 2, HEIGHT*1 / 8)
    draw_text(window, u"SPACECRAFT", int(HEIGHT / 10), WIDTH / 2, HEIGHT*1 / 4)
    draw_text(window, "SHMUP!", int(HEIGHT / 15), WIDTH / 2, HEIGHT*7 / 20)
    draw_text(window, "AUTHOR:GUOJINGXING\nMY YOUTUBE:c/jimkaku1999", int(HEIGHT / 30), WIDTH / 2, HEIGHT*9 / 20)
    draw_text(window, u"Press up down to control, enter space to shoot", int(HEIGHT / 15), WIDTH / 2, HEIGHT*11 / 20)
    draw_text(window, u"Press any key to start", int(HEIGHT / 10), WIDTH / 2, HEIGHT*15 / 20)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYUP:
                waiting = False

#制造玩家（飞机）
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 21
        #调整撞击圆圈的大小
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 5
        self.x_speed = 5
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        #游戏津贴超时
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            if self.power <= 1:
                self.power = 1
            self.power_timer = pygame.time.get_ticks()
        #如果是hidden就把它unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.x_speed = 0
        self.y_speed = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += self.y_speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT:
            self.y_speed = -5
        if self.rect.top < 0:
            self.y_speed = 5
        keystate = pygame.key.get_pressed()
        if keystate[K_LEFT] or keystate[K_a]:
            self.x_speed = -5
        if keystate[K_RIGHT] or keystate[K_d]:
            self.x_speed = 5
        if keystate[K_UP] or keystate[K_w]:
            self.y_speed = -5
        if keystate[K_DOWN] or keystate[K_s]:
            self.y_speed = 5
        if keystate[K_SPACE] or keystate[K_KP_ENTER]:
            self.shot()
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:#打出一发子弹
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:#打出两发子弹
                #从玩家的飞机的中间的两头发子弹
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

#制造敌人（敌机）        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        #self.image.fill(RED)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/ 2)
        #调整撞击圆圈的大小
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width, 30)
        self.rect.y = random.randrange(-80, -30)
        self.speedy = random.randrange(2, 6)
        self.speedx = random.randrange(-2, 2)
        self.last_update = pygame.time.get_ticks()
        self.rotspeed = random.randrange(-8, 8)
        self.rot = 0

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rotspeed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left > WIDTH + 10 or \
        self.rect.right < -10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width, 30)
            self.rect.y = random.randrange(-80, -30)
            self.speedy = random.randrange(2,6)
            self.speedx = random.randrange(1, 4)

#制造子弹（激光）
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y #子弹的底部坐标等于传进来的y坐标
        self.rect.centerx = x #子弹的中点x坐标等于传进来的x坐标
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #超出边界就被kill
        if self.rect.bottom < 0:
            self.kill()

#制造游戏津贴
class Powerups(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy
        #超出边界就被kill
        if self.rect.top > HEIGHT:
            self.kill()


#制造爆炸特效
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        #帧速度
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



#加载背景图片
background = pygame.image.load(os.path.join(space_holder,"backgrounds","purple.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#加载玩家、陨石、激光等
player_img = pygame.image.load(os.path.join(space_holder,"PNG","playerShip1_blue.png")).convert()
player_img.set_colorkey(BLACK)
player_mini = pygame.transform.scale(player_img, (25, 19))
meteor_images = []
meteors = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png', \
            'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', \
            'meteorBrown_tiny1.png', 'meteorBrown_tiny1.png']
for m in meteors:
    meteor_images.append(pygame.image.load(os.path.join(PNGS, "Meteors", m)).convert())
bullet_img = pygame.image.load(os.path.join(space_holder,"PNG","Lasers","laserBlue01.png")).convert()

#power-ups
powerup_img = {}
powerup_img['shield'] = pygame.image.load(os.path.join(powerup_dir, "shield_gold.png")).convert()
powerup_img['gun'] = pygame.image.load(os.path.join(powerup_dir, "bolt_gold.png")).convert()

#爆炸特效
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim['death'] = []
for i in range(9):
    path = os.path.join(explode_dir, "regularExplosion0{}.png".format(i))
    path2 = os.path.join(explode_dir, "sonicExplosion0{}.png".format(i))
    img = pygame.image.load(path).convert()
    img.set_colorkey(BLACK)
    #img_rect = img.get_rect()
    img_large = pygame.transform.scale(img, E_1)
    img_small = pygame.transform.scale(img, E_2)
    img_death = pygame.image.load(path2)
    img_death.set_colorkey(BLACK)
    explosion_anim["lg"].append(img_large)
    explosion_anim["sm"].append(img_small)
    explosion_anim['death'].append(img_death)

#加载声音
shoot_sound = pygame.mixer.Sound(os.path.join(sound,"Laser_Shoot.wav"))
player_die_sound = pygame.mixer.Sound(os.path.join(explode_dir, "rumble1.ogg"))

#加载背景音乐
pygame.mixer.music.load(os.path.join(sound, "bg.ogg"))
pygame.mixer.music.set_volume(0.4)

score = 0
pygame.mixer.music.play(loops=-1)
#游戏循环
game_over = True
running = True
while running:
    #是否游戏结束，或者开始游戏时的初始化
    if game_over:
        show_go_screen()
        #游戏矢量图组初始化
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(40):
            newmob()
        score = 0
        game_over = False
    #以正确的速度持续运行
    clock.tick(FPS)
    #进程输入
    for event in pygame.event.get():
        #检查是否要关闭窗口
        if event.type == QUIT:
            running = False
        #elif event.type == KEYDOWN:
            #if event.key == K_SPACE:
                #player.shot()


    #更新当前状态   
    all_sprites.update()
    
    #子弹击中敌人
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:    #每次被击中的时候
        #大的爆炸
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        newmob(count)
        score += 50 - hit.radius
        if random.random() < 0.4: #powerups出现的频率0-1之间
            powerup = Powerups(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    #被敌人击中
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) #sprite的圆圈
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        player.shield -= hit.radius*2
        newmob(count)
        if player.shield <= 0:
            player_die_sound.play()
            death = Explosion(hit.rect.center, "death")
            all_sprites.add(death)
            player.hide()
            player.lives -= 1
            player.shield = 100
            
    #玩家捡到游戏津贴
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30, 5)
            if player.shield > 100:
                player.shield = 100
        if hit.type == "gun":
            player.powerup()

    #玩家被打死 爆炸特效消失
    if player.lives == 0 and not death.alive():
        game_over = True

    #绘制 / 渲染(图层根据代码顺序叠加)
    window.fill(BLACK)
    window.blit(background, background_rect)
    all_sprites.draw(window)
    draw_text(window, "score: %05d"%score, 18, WIDTH / 4, 10)
    draw_shield_bar(window, WIDTH*2 / 3, 10, player.shield)
    draw_lives(window, WIDTH - 100, 10, player.lives, player_mini)
    #绘制了所有东西之后，flip整个屏幕
    pygame.display.flip()
    
pygame.quit()