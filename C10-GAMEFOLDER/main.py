import pygame as pg
from pygame.locals import *
import random as rd
from settings import *
from sprites import *

class Game:
    def __init__(self):
        #游戏初始化各种数据
        pg.init()
        pg.mixer.init()
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    
    def new(self):
        #开始一个新的游戏
        #创建sprite组
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        #游戏循环
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)#控制游戏帧数
            self.events()   #游戏中会碰到的事件
            self.update()   #更新游戏状态
            self.draw()     #绘制游戏画面

    def update(self):
        #游戏循环 - 更新游戏状态
        self.all_sprites.update()
        if self.player.v.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.v.y = 0

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

    def draw(self):
        #游戏循环 - 绘制游戏画面
        self.window.fill(BLACK)
        self.all_sprites.draw(self.window)
        #将整个display的surface对象更新到屏幕上去
        pg.display.flip()
    
    def show_start_screen(self):
        #开始游戏画面
        pass

    def show_go_screen(self):
        #继续游戏画面
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new() #新游戏
    g.show_go_screen() #继续游戏屏幕

pg.quit()