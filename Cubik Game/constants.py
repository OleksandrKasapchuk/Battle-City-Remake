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

tile_size = 64

#зображення
back = image.load("assets/images/fone.png")
start_background = transform.scale(back,(WIN_WIDTH,WIN_HEIGHT))
play_background = transform.scale(image.load("assets/images/mud.png"),(WIN_WIDTH,WIN_HEIGHT))

play_button = image.load("assets/images/play_button.png")
exit_button = image.load("assets/images/exit_button.png")

logo1 = transform.scale(image.load("assets/images/logo1.png"),(600,600))
logo2 = image.load("assets/images/logo2.png")


brick_img = image.load("assets/images/brick.png")
qw = image.load("assets/images/brick_b.png")
brick_b_img = transform.scale(qw, (tile_size, tile_size))

beton_img = image.load("assets/images/beton.png")
ice_img = image.load("assets/images/ice.png")
bush_img = image.load("assets/images/bush.png")
water_img = image.load("assets/images/water.png")

#кольори
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)
#музика
mixer.init()
mixer.music.load('assets/sounds/toto.ogg')

mixer.music.set_volume(0.2) 
fire_sound = mixer.Sound('assets/sounds/drobovik.wav')


mixer.music.set_volume(0.1)
mixer.music.play()
