#імпортуємо модулі
from logger import *
import pygame
from constants import *
from scenes import *
from sprites import *


logging.info(f'Програма була запущена')

pygame.init()  

clock = pygame.time.Clock()

APP = True
SCENE_GAME = True
play = True

#ігровий цикл
while APP:
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                APP = False
        #гра 
        if play:
            pygame.display.update()
            game.update()
        clock.tick(FPS)
