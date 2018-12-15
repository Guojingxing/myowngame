# 超级玛丽游戏之改编版 - 小兔跳跳跳
# 美术: kenney.nl
# 背景音乐： https://opengameart.org/content/happy-tune

import pygame as pg
import random as rd
from pygame.locals import *
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #游戏初始化各种数据
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT)
        self.load_data()

    def load_data(self):
        # 加载数据
        self.dir = path.dirname(__file__)
        sprite_dir = path.join(self.dir, 'Spritesheets')
        self.img_dir = path.join(self.dir, 'img')
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(self.img_dir, "cloud{}.png".format(i))).convert())
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(sprite_dir, SPRITESHEET))
        self.snd_dir = path.join(self.dir, 'sound')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump1.wav'))
        self.die_sound1 = pg.mixer.Sound(path.join(self.snd_dir, "die.wav"))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'speedup.wav'))
        
    def set_title_image(self): 
        self.title_image = pg.image.load(path.join(self.img_dir, "logo.png")).convert()
        self.title_image.set_colorkey(BLACK)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = WIDTH/2+300, HEIGHT/2+50
        self.t_w, self.t_h = self.title_rect.width//2, self.title_rect.height//2
        self.title_image = pg.transform.scale(self.title_image,(self.t_w, self.t_h))
        self.screen.blit(self.title_image, self.title_rect)


    def new(self):
        #开始一个新的游戏
		#创建sprite组
        self.score = 0 #初始化分数
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        #self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST: #获取平台列表中的平台
            Platform(self, *plat) # p =
            #self.all_sprites.add(p)
            #self.platforms.add(p)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'bgm.ogg'))
        for i in range(5):
            c = Cloud(self)
            c.rect.x -= WIDTH
        self.run()

    def run(self):
        #游戏循环
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)	#控制游戏帧数
            self.events()			#游戏中会碰到的事件
            self.update()			#更新游戏状态
            self.draw()				#绘制游戏画面
        pg.mixer.music.fadeout(500)     #游戏结束音乐逐渐消失（500毫秒）

    def update(self):
        #游戏循环 - 更新游戏状态
        self.all_sprites.update()

        #if self.player.vel.x > 0: #走的距离等于分数
            #self.score += self.player.vel.x

        # 产生一个敌人
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + rd.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # 检查玩家是否碰到平台（只在掉落的时候）
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit #检测撞击到的平台哪个最低
                #if self.player.pos.x < lowest.rect.right and \
                   #self.player.pos.x > lowest.rect.left: #小兔到达边缘的时候掉下去
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
                self.player.walking = True
        
        #宽度到达 width/2 时屏幕整体左移动
        if self.player.pos.x > WIDTH / 2: 
            if rd.randrange(100) < 1:
                Cloud(self)

            self.player.pos.x += -max(abs(self.player.vel.x),2)
            for plat in self.platforms: #平台跟着移动
                plat.rect.x += -max(abs(self.player.vel.x),2)
                if plat.rect.right < 0: #平台移出左屏幕就kill
                    plat.kill()

            for powerup in self.powerups:   #津贴跟着移动
                powerup.rect.x += -max(abs(self.player.vel.x),2)
                if powerup.rect.right < 0:
                    powerup.kill()
                    self.score += 10

            for mob in self.mobs:
                mob.rect.x += -max(abs(self.player.vel.x),2)
                if mob.rect.right < 0: #敌人移出左屏幕就kill
                    mob.kill()

            r = rd.choice([2, 2.5, 3, 3.5])
            for cloud in self.clouds: #云彩的移动
                cloud.rect.x += -max(abs(self.player.vel.x / r),2)
                if cloud.rect.right < 0: 
                    cloud.kill()

        #玩家die
        if self.player.rect.bottom > HEIGHT and self.player.rect.bottom < HEIGHT + 30: 
            pg.mixer.music.stop()
            self.die_sound1.play()
            #for sprite in self.all_sprites:
                #pass #对所有的sprite后事处理(无)
        if self.player.rect.bottom > HEIGHT + 5000:
            self.playing = False
        
        #玩家捡到游戏津贴
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.pos.x += BOOST_POWER*10
                self.player.pos.y = 100
                self.score += 50
                self.player.jumping = False

        #玩家碰到敌人
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.die_sound1.play()
            pg.mixer.music.stop()
            self.playing = False
        

        #随机产生平台
        while len(self.platforms) < 12:
            p = Platform2(self, rd.randrange(1280, 1880, 200),
                         rd.randrange(int(HEIGHT/4), HEIGHT - 120, 180))
            hits = pg.sprite.spritecollide(p, self.platforms, False)
            if not hits:
                self.platforms.add(p)
                self.all_sprites.add(p)

    def events(self):
        #游戏循环 - 游戏中会碰到的事件
        for event in pg.event.get():
            #检查是否要关闭窗口
            if event.type == QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    self.player.jump()
            if event.type == KEYUP:
                if event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    self.player.jump_cut()

    def draw(self):
        #游戏循环 - 绘制游戏画面
        self.screen.fill(SKYBLUE)
        self.all_sprites.draw(self.screen)
        #self.screen.blit(self.player.image, self.player.rect)
        self.draw_text_up("BUNNY", int(HEIGHT/20), WHITE, 0.06*WIDTH, 0.06*HEIGHT)
        self.draw_text_up("%06d"%self.score, int(HEIGHT/20), WHITE, 0.06*WIDTH, (0.06+1/20)*HEIGHT)
        #将整个display的surface对象更新到屏幕上去
        pg.display.flip()

    def draw_text_up(self, text, size= int(HEIGHT/20), color=WHITE, x=WIDTH/2, y = 15):
        #文本显示（上方）
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text, size= int(HEIGHT/20), color=WHITE, x=WIDTH/2, y = 15):
        #文本显示
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.running = False
                if event.type == KEYUP:
                    if event.key == K_KP_ENTER or event.key == K_SPACE or K_RETURN:
                        waiting = False

    def show_start_screen(self):
        #开始游戏画面
        self.screen.fill(BGCOLOR)
        self.set_title_image()
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2+100)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        #继续游戏画面
        if not self.running:
            return
        #self.screen.fill(SKYBLUE)
        self.draw_text("GAME OVER", 100, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(int(self.score)), 44, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 44, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(int(self.score)))
        else:
            self.draw_text("High Score: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

g = Game()
g.show_start_screen()
while g.running:
    g.new()	#新游戏
    g.show_go_screen()#继续游戏屏幕

pg.quit()