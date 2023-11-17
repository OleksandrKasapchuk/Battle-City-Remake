#імпортуємо модулі
import os
from pygame import *
#розміри вікна
WIN_WIDTH = 832
WIN_HEIGHT = 832
#створення вікна
WINDOW = display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCENE_GAME = 0
SCENE_MAIN = 1

FPS = 30

fired = False
max_health=3

log_file = "log.txt"
#кольори
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)
#музика
mixer.init()
mixer.music.load('assets/sounds/toto.wav')
mixer.music.set_volume(0.2) 
fire_sound = mixer.Sound('assets/sounds/drobovik.wav')
mixer.music.set_volume(0.1)
mixer.music.play()
