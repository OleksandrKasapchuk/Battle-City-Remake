import os
from pygame import *

WIN_WIDTH = 832
WIN_HEIGHT = 832

WINDOW = display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCENE_GAME = 0
SCENE_MAIN = 1

FPS = 30

fired = False

log_file = "log.txt"

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)

#PATH
PATH = os.path.dirname(__file__) + os.sep
PATH_ASSETS = PATH + "assets" + os.sep
PATH_IMAGES = PATH_ASSETS + 'images' + os.sep
PATH_AUDIOS = PATH_ASSETS + ''
