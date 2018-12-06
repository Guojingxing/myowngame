# pygame模板 - 开始一个新的pygame项目
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# 定义默认颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 初始化pygame 创建新窗口
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
# 游戏循环
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # 更新
    all_sprites.update()

    # 绘制 / 渲染
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # 绘制了所有东西 *之后*, flip the display（翻转屏幕）
    pygame.display.flip()

pygame.quit()
