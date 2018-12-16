# 超级玛丽游戏之改编版 - 小兔跳跳跳 1.0版
# 美术: kenney.nl
# 背景音乐： https://opengameart.org/content/happy-tune
# 作者： Guojingxing

import pygame as pg
import random as rd
from pygame.locals import *
from settings import *
from sprites import *
from os import path
from maps import *

class Game:
    def __init__(self):
        #游戏初始化各种数据
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.lives = 5
        self.c_score = 0
        self.b_score = 0
        self.s_score = 0
        self.g_score = 0
        self.game_over = False
        self.font_name = pg.font.match_font(FONT)
        self.load_data()

    def load_data(self):
        # 加载数据
        self.dir = path.dirname(__file__)
        sprite_dir = path.join(self.dir, 'Spritesheets')

        #导入图片地址
        self.img_dir = path.join(self.dir, 'img')

        #导入云彩图片
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(self.img_dir, "cloud{}.png".format(i))).convert())
        
        #导入分数
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        
        #统一图片路径
        self.spritesheet = Spritesheet(path.join(sprite_dir, SPRITESHEET))
        self.snd_dir = path.join(self.dir, 'sound')

        #声音路径
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump1.wav'))
        self.die_sound1 = pg.mixer.Sound(path.join(self.snd_dir, "die.wav"))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'speedup.wav'))
        self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'coin.wav'))
        self.up_sound = pg.mixer.Sound(path.join(self.snd_dir, 'up.wav'))

        #导入HUD(屏幕最上方显示命、显示硬币数和胡萝卜数)
        hud = path.join(self.img_dir, 'HUD')
        self.show_carrot = pg.image.load(path.join(hud, 'carrots.png')).convert()
        self.show_carrot.set_colorkey(BLACK)
        self.show_carrot_rect = self.show_carrot.get_rect()
        self.show_carrot = pg.transform.scale(self.show_carrot, (30, 30))
        self.show_carrot_rect.x = 0.2*WIDTH + 15
        self.show_carrot_rect.y = 0.06*HEIGHT

        self.show_b_coin = pg.image.load(path.join(hud, 'coin_bronze.png')).convert()
        self.show_b_coin.set_colorkey(BLACK)
        self.show_b_coin_rect = self.show_carrot.get_rect()
        self.show_b_coin = pg.transform.scale(self.show_b_coin, (30, 30))
        self.show_b_coin_rect.x = 0.4*WIDTH + 15
        self.show_b_coin_rect.y = 0.06*HEIGHT

        self.show_s_coin = pg.image.load(path.join(hud, 'coin_silver.png')).convert() 
        self.show_s_coin.set_colorkey(BLACK)
        self.show_s_coin_rect = self.show_carrot.get_rect()
        self.show_s_coin = pg.transform.scale(self.show_s_coin, (30, 30))
        self.show_s_coin_rect.x = 0.6*WIDTH + 15
        self.show_s_coin_rect.y = 0.06*HEIGHT
        
        self.show_g_coin = pg.image.load(path.join(hud, 'coin_gold.png')).convert() 
        self.show_g_coin.set_colorkey(BLACK)
        self.show_g_coin_rect = self.show_carrot.get_rect()
        self.show_g_coin = pg.transform.scale(self.show_g_coin, (30, 30))
        self.show_g_coin_rect.x = 0.8*WIDTH + 15
        self.show_g_coin_rect.y = 0.06*HEIGHT

        self.show_life = pg.image.load(path.join(hud, 'lifes.png')).convert()
        self.show_life.set_colorkey(BLACK)
        self.show_life_rect = self.show_carrot.get_rect()
        self.show_life = pg.transform.scale(self.show_life, (26, 35))
        
    def set_title_image(self): 
        self.title_image = pg.image.load(path.join(self.img_dir, "logo.png")).convert()
        self.title_image.set_colorkey(BLACK)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = WIDTH/2+300, HEIGHT/2+50
        self.t_w, self.t_h = self.title_rect.width//2, self.title_rect.height//2
        self.title_image = pg.transform.scale(self.title_image,(self.t_w, self.t_h))
        self.screen.blit(self.title_image, self.title_rect)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30*i
            img_rect.y = y
            surf.blit(img, img_rect)

    def new(self):
        #开始一个新的游戏

		#创建sprite组
        self.score = 0 #初始化分数

        # 游戏道具的分数
        self.carrot_num = 0
        self.bcoin_num = 0
        self.gcoin_num = 0
        self.scoin_num = 0

        self.world = 1 #设立初始关卡
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        self.carrots = pg.sprite.Group()
        self.bronzes = pg.sprite.Group()
        self.silvers = pg.sprite.Group()
        self.golds = pg.sprite.Group()

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
        self.choose_world()
        self.run()

    def choose_world(self):
        #选择世界（无）
        pass

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

        if self.lives > 5:
            self.lives = 5
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

            
            for carrot in self.carrots:   #萝卜跟着移动
                carrot.rect.x += -max(abs(self.player.vel.x),2)
                if carrot.rect.right < 0:
                    carrot.kill()
            for bronze in self.bronzes:   #铜跟着移动
                bronze.rect.x += -max(abs(self.player.vel.x),2)
                if bronze.rect.right < 0:
                    bronze.kill()
            for silver in self.silvers:   #银跟着移动
                silver.rect.x += -max(abs(self.player.vel.x),2)
                if silver.rect.right < 0:
                    silver.kill()
            for gold in self.golds:   #金跟着移动
                gold.rect.x += -max(abs(self.player.vel.x),2)
                if gold.rect.right < 0:
                    gold.kill()


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
        if self.player.rect.top > HEIGHT:
            self.playing = False
            self.lives -= 1

        #彻底退出游戏
        if self.lives == 0:
            self.playing == False
            self.game_over = True
        
        #玩家捡到游戏津贴
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                #self.player.pos.x += BOOST_POWER*10
                #self.player.pos.y = 100
                self.score += 500
                self.player.jumping = False


        carrot_hits = pg.sprite.spritecollide(self.player, self.carrots, True)
        for carrot in carrot_hits:
            if carrot.type == 'carrot':
                self.up_sound.play()
                self.score += 1000
                self.c_score += 1
                self.lives += 1
        bronze_hits = pg.sprite.spritecollide(self.player, self.bronzes, True)
        for bronze in bronze_hits:
            if bronze.type == 'bronze':
                self.coin_sound.play()
                self.score += 100
                self.b_score += 1
        silver_hits = pg.sprite.spritecollide(self.player, self.silvers, True)
        for silver in silver_hits:
            if silver.type == 'silver':
                self.coin_sound.play()
                self.score += 300
                self.s_score += 1
        gold_hits = pg.sprite.spritecollide(self.player, self.golds, True)
        for gold in gold_hits:
            if gold.type == 'gold':
                self.coin_sound.play()
                self.score += 500
                self.g_score += 1
                self.lives = 5


        #玩家碰到敌人
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.die_sound1.play()
            pg.mixer.music.stop()
            self.playing = False
            self.lives -= 1
        

        #随机产生平台
        while len(self.platforms) < 18:
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
        self.screen.blit(self.show_carrot, self.show_carrot_rect)
        self.draw_text_up("%03d"%self.c_score, int(HEIGHT/20), WHITE, 0.2*WIDTH, (0.06+1/20)*HEIGHT)
        self.screen.blit(self.show_b_coin, self.show_b_coin_rect)
        self.draw_text_up("%03d"%self.b_score, int(HEIGHT/20), WHITE, 0.4*WIDTH, (0.06+1/20)*HEIGHT)
        self.screen.blit(self.show_s_coin, self.show_s_coin_rect)
        self.draw_text_up("%03d"%self.s_score, int(HEIGHT/20), WHITE, 0.6*WIDTH, (0.06+1/20)*HEIGHT)
        self.screen.blit(self.show_g_coin, self.show_g_coin_rect)
        self.draw_text_up("%03d"%self.g_score, int(HEIGHT/20), WHITE, 0.8*WIDTH, (0.06+1/20)*HEIGHT)
        self.draw_lives(self.screen, WIDTH - 150, 10, self.lives, self.show_life)
        #self.draw_text_up()
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
        self.draw_text("Score: " + str(int(self.score)), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Carrot: " + str(int(self.c_score)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 65)
        self.draw_text("Bronze: " + str(int(self.b_score)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 90)
        self.draw_text("Silver: " + str(int(self.s_score)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 115)
        self.draw_text("Gold: " + str(int(self.g_score)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 140)
        self.draw_text("Press a key to play again", 44, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 30)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(int(self.score)))
        else:
            self.draw_text("High Score: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 30)
        pg.display.flip()
        self.wait_for_key()

    def game_over_screen(self):
        if not self.running:
            return
        #self.screen.fill(SKYBLUE)
        self.draw_text("GAME OVER", 100, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(int(self.score)), 44, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to return to the start screen", 44, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            #self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            self.draw_text("High Score: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(int(self.score)))
        else:
            self.draw_text("High Score: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        self.game_over = False
        self.lives = 5
        

g = Game()
g.show_start_screen()
while g.running:
    g.new()	#新游戏
    if g.playing == False and g.game_over == False:
        g.show_go_screen()#继续游戏屏幕
    if g.playing == False and g.game_over == True:
        g.game_over_screen()

pg.quit()