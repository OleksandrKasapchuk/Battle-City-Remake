import os
from pygame import *

WIN_WIDTH = 1200
WIN_HEIGHT = 800

WINDOW = display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCENE_GAME = 0
SCENE_MAIN = 1

FPS = 30

BLUE_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)

#PATH
PATH = os.path.dirname(__file__) + os.sep
PATH_ASSETS = PATH + "assets" + os.sep
PATH_IMAGES = PATH_ASSETS + 'images' + os.sep
PATH_AUDIOS = PATH_ASSETS + ''
