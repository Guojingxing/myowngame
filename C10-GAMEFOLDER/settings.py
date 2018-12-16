
#游戏屏幕
TITLE = "小兔跳跳跳"
WIDTH = 1280
HEIGHT = 720
FPS = 60	#游戏帧速率

FONT = "arial"  #字体
#玩家速度、加速度等属性
PLAYER_ACC = 0.5	 #加速度
PLAYER_FRICTION = -0.12	#摩擦力/阻力
PLAYER_GRAV = 0.8	#重力加速度
PLAYER_JUMP = 20    #向上的初速度

# game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# 平台列表 - Super Mario 随机产生需要的所有的平台
# (x,   y)
PLATFORM_LIST = []
for i in range(0, 2200, 200):#底部平台
    PLATFORM_LIST.append((i, HEIGHT - 60))
    #PLATFORM_LIST.append((i, HEIGHT - 30))

for plat in [(700, HEIGHT * 3 / 4),
            (1930, HEIGHT - 60),
            (1150, 200),
            (975, 400)]:
    PLATFORM_LIST.append(plat)

#颜色配置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (92, 148, 252)
PURPLE = (0, 255, 255)

BGCOLOR = SKYBLUE
DARK_BGCOLOR = (21, 21, 67)

#保存最高分数/文件
HS_FILE = 'highscore.txt'
SPRITESHEET = 'spritesheet_jumper.png'