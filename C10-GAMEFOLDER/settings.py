#游戏配置文件
#游戏屏幕
WIDTH = 1280
HEIGHT = 720
TITLE = u"超级玛丽升级版"

#颜色配置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#游戏帧速率
FPS = 60

#玩家速度、加速度等属性
PLAYER_ACC = 1        #加速度
PLAYER_FRICTION = -0.12  #摩擦力/阻力
PLAYER_GRAV = 0.5 #重力加速度

#平台列表
PLATFORM_LIST = [
    (0, 9*HEIGHT/10, WIDTH, 1*HEIGHT/10),
    (WIDTH/2 - 50, HEIGHT *3/4, 100, 20),
    (125, HEIGHT - 350, 100, 20),
    (350, 200, 100, 20),
    (200, 150, 50, 20)
]
